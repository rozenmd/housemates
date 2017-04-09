from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from group.models import Group
from payments.models import Payment
from bills.models import Bill
from web.models import MyProfile
from django.core import serializers
from django_pandas.io import read_frame
import pandas as pd


def dashboard(request, template_name='web/dashboard.html'):
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    data = {'current_group': current_group}

    if current_group:
        bills = Bill.objects.filter(group=current_group)
        payments = Payment.objects.filter(group=current_group)

        qs = bills
        cols = ['id','created', 'who_paid', 'quantity_paid', 'who_owes__member']
        df = read_frame(qs, cols, verbose=True)
        bills = df.to_json(orient='records')
        data['bills'] = bills



        qs = payments
        df = read_frame(qs)
        payments = df.to_json(orient='records')
        data['payments'] = payments
    return render(request, template_name, data)
