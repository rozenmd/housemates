from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped

# Create your models here.


class Household(TimeStamped):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, unique=False)

    def __str__(self):
        return self.name


class HouseholdMember(TimeStamped):
    household = models.ForeignKey(Household, related_name='household_member')
    member = models.ForeignKey(User, related_name='household')

    def __str__(self):
        return self.member.username


class Payment(TimeStamped):
    from_user = models.ForeignKey(User, related_name='payment_made')
    to_user = models.ForeignKey(User, related_name='payment_received')


class Bill(TimeStamped):
    who_paid = models.ForeignKey(User, related_name='bill_paid')
    description = models.TextField()
    quantity_paid = models.DecimalField(max_digits=10, decimal_places=2)
