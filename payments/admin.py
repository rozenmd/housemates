from django.contrib import admin

# Register your models here.
from payments.models import Payment

admin.site.register(Payment)