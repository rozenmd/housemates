from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from mezzanine.core.models import TimeStamped


class Group(TimeStamped):
    name = models.CharField(max_length=255, unique=True, verbose_name='Group Name')
    password = models.CharField(max_length=255, unique=False)

    def __str__(self):
        return self.name


class GroupMember(TimeStamped):
    group = models.ForeignKey(Group, related_name='group_member')
    member = models.ForeignKey(User, related_name='group')

    class Meta:
        unique_together = ('group', 'member',)

    def __str__(self):
        return self.member.username
