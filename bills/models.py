from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped

# Create your models here.



class Payment(TimeStamped):
    from_user = models.ForeignKey(User, related_name='payment_made')
    to_user = models.ForeignKey(User, related_name='payment_received')


class Bill(TimeStamped):
    who_paid = models.ForeignKey(User, related_name='bill_paid')
    description = models.TextField()
    quantity_paid = models.DecimalField(max_digits=10, decimal_places=2)
