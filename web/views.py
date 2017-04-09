from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from group.models import Group
from payments.models import Payment
from bills.models import Bill
from web.models import MyProfile


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
        
        data['bills'] = bills
        data['payments'] = payments

    return render(request, template_name, data)
