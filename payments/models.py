from __future__ import unicode_literals

from django.db import models

# Create your models here.
from mezzanine.core.models import TimeStamped

from group.models import GroupMember, Group


class Payment(TimeStamped):
    from_user = models.ForeignKey(GroupMember, related_name='payment_made')
    to_user = models.ForeignKey(GroupMember, related_name='payment_received')
    group = models.ForeignKey(Group, related_name='payment')
    quantity_paid = models.FloatField()
