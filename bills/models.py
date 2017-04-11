from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped
from group.models import Group, GroupMember
# Create your models here.




class Bill(TimeStamped):
    who_paid = models.ForeignKey(GroupMember, related_name='bill_paid')
    description = models.TextField()
    quantity_paid = models.FloatField()
    group = models.ForeignKey(Group, related_name='bill')
    who_owes = models.ManyToManyField(GroupMember)

# class Debt(TimeStamped):
#     who_incurred_cost = models.ForeignKey(HouseholdMember, related_name='money_owed')
#     bill = models.ForeignKey(Bill, related_name='who_owes')
