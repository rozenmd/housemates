from __future__ import unicode_literals

from django.db import models
from mezzanine.conf import settings
from mezzanine.core.models import TimeStamped
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.context import RequestContext
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .managers import InvitationManager
from .app_settings import app_settings
from .adapters import get_invitations_adapter
from . import signals
from group.models import Group


class MyProfile(TimeStamped):
    user = models.OneToOneField("auth.User")
    current_group = models.IntegerField(null=True)
    # name = models.CharField(max_length=255)


@python_2_unicode_compatible
class Invitation(TimeStamped):

    email = models.EmailField(unique=False, verbose_name=_('e-mail address'),
                              max_length=app_settings.EMAIL_MAX_LENGTH)
    accepted = models.BooleanField(verbose_name=_('accepted'), default=False)
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    objects = InvitationManager()

    @classmethod
    def create(cls, email, group=None, inviter=None):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key,
            inviter=inviter,
            group=group)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = (kwargs['site'] if 'site' in kwargs
                        else Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)

        ctx = RequestContext(request, {
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'group': self.group,
            'key': self.key,
            'inviter': self.inviter,
        })

        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter)

    def __str__(self):
        return "Invite: {0}".format(self.email)
