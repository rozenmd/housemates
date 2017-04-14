from decimal import *
from django.shortcuts import render, get_object_or_404
from group.models import Group, GroupMember
from payments.models import Payment
from bills.models import Bill
from web.models import MyProfile
from django_pandas.io import read_frame
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView, HighchartPlotLineChartView
import json
from django.views.generic import FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from braces.views import LoginRequiredMixin
from .forms import InviteForm, CleanEmailMixin
from .models import Invitation
from .exceptions import AlreadyInvited, AlreadyAccepted, UserRegisteredEmail
from .app_settings import app_settings
from .adapters import get_invitations_adapter
from .signals import invite_accepted
from mezzanine.accounts.urls import SIGNUP_URL, LOGIN_URL



def dashboard(request, template_name='web/dashboard.html'):
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    data = {'current_group': current_group}

    if current_group:
        bills = Bill.objects.filter(group=current_group)
        payments = Payment.objects.filter(group=current_group)
        members = GroupMember.objects.filter(group=current_group)
        # Calculate the total owed per bill first:
        bill_dict = {}


        for member in members:
            bill_dict[str(member)] = 0.0
        for bill in bills:

            number_owing = float(len(bill.who_owes.all()))
            bill_per_person = bill.quantity_paid/number_owing

            for debtor in bill.who_owes.all():
                if debtor == bill.who_paid:
                    bill_dict[str(debtor)] += bill_per_person-bill.quantity_paid
                else:# str(debtor) in bill_dict:
                    bill_dict[str(debtor)] += bill_per_person
        for payment in payments:
            bill_dict[str(payment.from_user)] -= payment.quantity_paid
            bill_dict[str(payment.to_user)] += payment.quantity_paid
        for key, value in bill_dict.items():
            bill_dict[key] = Decimal(Decimal(value).quantize(Decimal('.01'), rounding=ROUND_UP))

        # bill_dict = simplejson.dumps(bill_dict)
        qs = bills
        cols = ['id', 'created', 'who_paid', 'quantity_paid', 'who_owes__member']
        df = read_frame(qs, cols, verbose=True)
        bills = df.to_json(orient='records')
        data['bills'] = bills
        data['lah'] = bill_dict


        qs = payments
        df = read_frame(qs)
        payments = df.to_json(orient='records')
        data['payments'] = payments

    return render(request, template_name, data)


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()


def homepage_view(request, template_name='index.html'):
    if request.user.is_authenticated:
        invitations = Invitation.objects.filter(email=request.user.email)
        if len(invitations) > 0:
            for invite in invitations:
                if not GroupMember.objects.filter(group=invite.group.id, member=request.user.id):
                    GroupMember(group=invite.group, member=request.user).save()
                    messages.add_message(request, messages.INFO, 'You have been added to the group: '+invite.group+'!')

    return render(request, template_name)


def send_invite(request, template_name='invitations/forms/_invite.html'):
    groups = Group.objects.filter(group_member__member=request.user)
    form = InviteForm(request.POST or None)
    form.fields['group'].queryset = groups

    if form.is_valid():
        email = form.cleaned_data["email"]
        group = form.cleaned_data["group"]

        invite = form.save()
        invite.inviter = request.user
        invite.save()
        invite.send_invitation(request)
        messages.add_message(request, messages.INFO, '%s has been invited' % email)

        return redirect('group_manage_members', group.id)
    data = {'form': form}
    return render(request, template_name, data)



class SendJSONInvite(LoginRequiredMixin, View):
    http_method_names = [u'post']

    def dispatch(self, request, *args, **kwargs):
        if app_settings.ALLOW_JSON_INVITES:
            return super(SendJSONInvite, self).dispatch(
                request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        status_code = 400
        invitees = json.loads(request.body.decode())
        response = {'valid': [], 'invalid': []}
        if isinstance(invitees, list):
            for invitee in invitees:
                try:
                    validate_email(invitee)
                    CleanEmailMixin().validate_invitation(invitee)
                    invite = Invitation.create(invitee)
                except(ValueError, KeyError):
                    pass
                except(ValidationError):
                    response['invalid'].append({
                        invitee: 'invalid email'})
                except(AlreadyAccepted):
                    response['invalid'].append({
                        invitee: 'already accepted'})
                except(AlreadyInvited):
                    response['invalid'].append(
                        {invitee: 'pending invite'})
                except(UserRegisteredEmail):
                    response['invalid'].append(
                        {invitee: 'user registered email'})
                else:
                    invite.send_invitation(request)
                    response['valid'].append({invitee: 'invited'})

        if response['valid']:
            status_code = 201

        return HttpResponse(
            json.dumps(response),
            status=status_code, content_type='application/json')


class AcceptInvite(SingleObjectMixin, View):
    form_class = InviteForm

    def get_signup_redirect(self):
        return SIGNUP_URL
        #app_settings.SIGNUP_REDIRECT

    def get(self, *args, **kwargs):
        if app_settings.CONFIRM_INVITE_ON_GET:
            return self.post(*args, **kwargs)
        else:
            raise Http404()

    def post(self, *args, **kwargs):
        self.object = invitation = self.get_object()

        # Compatibility with older versions: return an HTTP 410 GONE if there
        # is an error. # Error conditions are: no key, expired key or
        # previously accepted key.
        if app_settings.GONE_ON_ACCEPT_ERROR and \
                (not invitation or
                 (invitation and (invitation.accepted or
                                  invitation.key_expired()))):
            return HttpResponse(status=410)

        # No invitation was found.
        if not invitation:
            # Newer behavior: show an error message and redirect.
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_invalid.txt')
            return redirect(LOGIN_URL)

        # The invitation was previously accepted, redirect to the login
        # view.
        if invitation.accepted:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_already_accepted.txt',
                {'email': invitation.email})
            # Redirect to login since there's hopefully an account already.
            return redirect(LOGIN_URL)

        # The key was expired.
        if invitation.key_expired():
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_expired.txt',
                {'email': invitation.email})
            # Redirect to sign-up since they might be able to register anyway.
            return redirect(self.get_signup_redirect())

        # The invitation is valid.
        # Mark it as accepted now if ACCEPT_INVITE_AFTER_SIGNUP is False.
        if not app_settings.ACCEPT_INVITE_AFTER_SIGNUP:
            accept_invitation(invitation=invitation,
                              request=self.request,
                              signal_sender=self.__class__)

        get_invitations_adapter().stash_verified_email(
            self.request, invitation.email)

        return redirect(self.get_signup_redirect())

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except Invitation.DoesNotExist:
            return None

    def get_queryset(self):
        return Invitation.objects.all()


def accept_invitation(invitation, request, signal_sender):
    invitation.accepted = True
    invitation.save()
    invite_accepted.send(sender=signal_sender, email=invitation.email)

    get_invitations_adapter().add_message(
        request,
        messages.SUCCESS,
        'invitations/messages/invite_accepted.txt',
        {'email': invitation.email})


def accept_invite_after_signup(sender, request, user, **kwargs):
    invitation = Invitation.objects.filter(email=user.email).first()
    if invitation:
        accept_invitation(invitation=invitation,
                          request=request,
                          signal_sender=Invitation)


if app_settings.ACCEPT_INVITE_AFTER_SIGNUP:
    signed_up_signal = get_invitations_adapter().get_user_signed_up_signal()
    signed_up_signal.connect(accept_invite_after_signup)