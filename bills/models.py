from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped
from household.models import Household, HouseholdMember
# Create your models here.



class Payment(TimeStamped):
    from_user = models.ForeignKey(HouseholdMember, related_name='payment_made')
    to_user = models.ForeignKey(HouseholdMember, related_name='payment_received')
    household = models.ForeignKey(Household, related_name='payment')


class Bill(TimeStamped):
    who_paid = models.ForeignKey(HouseholdMember, related_name='bill_paid')
    description = models.TextField()
    quantity_paid = models.DecimalField(max_digits=10, decimal_places=2)
    household = models.ForeignKey(Household, related_name='bill')
