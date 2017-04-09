from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped
from group.models import Group, GroupMember
# Create your models here.



class Payment(TimeStamped):
    from_user = models.ForeignKey(GroupMember, related_name='payment_made')
    to_user = models.ForeignKey(GroupMember, related_name='payment_received')
    group = models.ForeignKey(Group, related_name='payment')


class Bill(TimeStamped):
    who_paid = models.ForeignKey(GroupMember, related_name='bill_paid')
    description = models.TextField()
    quantity_paid = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(Group, related_name='bill')
    who_owes = models.ManyToManyField(GroupMember)

# class Debt(TimeStamped):
#     who_incurred_cost = models.ForeignKey(HouseholdMember, related_name='money_owed')
#     bill = models.ForeignKey(Bill, related_name='who_owes')
