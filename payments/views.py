from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from payments.models import Payment
from group.models import GroupMember, Group
from payments.forms import PaymentForm
from web.models import MyProfile


# Create your views here.

def payments_list(request, template_name='payments/payments_list.html'):
    groups = Group.objects.filter(group_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0 and profile.first().current_group:
        current_group = get_object_or_404(Group, pk=profile.first().current_group.id)
    else:
        current_group = ''
    data = {'current_group': current_group}

    match = GroupMember.objects.filter(member=request.user)
    if match:
        payments = Payment.objects.filter(group=current_group)

        data['object_list'] = payments
        return render(request, template_name, data)
    else:
        return HttpResponse("""
        <h1>You need to join or create a group!</h1>
        <button onclick="goBack()">Go Back</button>

        <script>
        function goBack() {
            window.history.back();
        }
        </script>
        """)


def payments_create(request, template_name='payments/payments_form.html'):
    groups = Group.objects.filter(group_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    data = {'current_group': current_group}
    match = GroupMember.objects.filter(member=request.user)
    if match:
        payments = Payment.objects.filter(group=current_group)
        data['object_list'] = payments

    form = PaymentForm(request.POST or None, initial={'group': current_group})
    form.fields['from_user'].queryset = GroupMember.objects.filter(group=current_group)
    form.fields['to_user'].queryset = GroupMember.objects.filter(group=current_group)
    if form.is_valid():
        form.save()
        return redirect('payments_list')
    data['form'] = form
    return render(request, template_name, data)


def payments_read(request, pk, template_name='payments/payments_view.html'):
    payments = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, instance=payments)
    if form.is_valid():
        form.save()
        return redirect('payments_list')
    return render(request, template_name, {'form': form})


def payments_update(request, pk, template_name='payments/payments_form.html'):
    payments = get_object_or_404(Payment, pk=pk)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    form = PaymentForm(request.POST or None, instance=payments)
    form.fields['from_user'].queryset = GroupMember.objects.filter(group=current_group)
    form.fields['to_user'].queryset = GroupMember.objects.filter(group=current_group)
    if form.is_valid():
        form.save()
        return redirect('payments_list')
    return render(request, template_name, {'form': form})


def payments_delete(request, pk, template_name='payments/payments_confirm_delete.html'):
    payments = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payments.delete()
        return redirect('payments_list')
    return render(request, template_name, {'object': payments})

