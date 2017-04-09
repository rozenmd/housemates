from __future__ import unicode_literals

from django.db import models

class MyProfile(models.Model):
    user = models.OneToOneField("auth.User")
    current_group = models.IntegerField(null=True)
    # name = models.CharField(max_length=255)
