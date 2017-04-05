from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped


class Household(TimeStamped):
    name = models.CharField(max_length=255, unique=True, verbose_name='Household Name')
    password = models.CharField(max_length=255, unique=False)

    def __str__(self):
        return self.name


class HouseholdMember(TimeStamped):
    household = models.ForeignKey(Household, related_name='household_member')
    member = models.ForeignKey(User, related_name='household')

    class Meta:
        unique_together = ('household', 'member',)

    def __str__(self):
        return self.member.username
