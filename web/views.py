from decimal import *

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from group.models import Group, GroupMember
from payments.models import Payment
from bills.models import Bill
from web.models import MyProfile
from django.core import serializers
from django_pandas.io import read_frame
import pandas as pd
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import simplejson
from chartjs.colors import next_color, COLORS
from chartjs.views.columns import BaseColumnsHighChartsView
from chartjs.views.lines import BaseLineChartView, HighchartPlotLineChartView
from chartjs.views.pie import HighChartPieView, HighChartDonutView


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
        members = GroupMember.objects.filter(group=current_group)
        # Calculate the total owed per bill first:
        bill_dict = {}
        for member in members:
            bill_dict[str(member)] = 0
        for bill in bills:
            number_owing = Decimal(len(bill.who_owes.all()))
            q = bill.quantity_paid
            r = number_owing
            p = q/r
            p = (p.quantize(Decimal('.001'), rounding=ROUND_05UP)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
            bill_per_person = p

            for debtor in bill.who_owes.all():
                if debtor == bill.who_paid:
                    bill_dict[str(debtor)] += bill_per_person-bill.quantity_paid#They've already paid
                elif str(debtor) in bill_dict:
                    bill_dict[str(debtor)] += bill_per_person
        for payment in payments:
            bill_dict[str(payment.from_user)] -= payment.quantity_paid
            bill_dict[str(payment.to_user)] += payment.quantity_paid
        lists = []

        # bill_dict = simplejson.dumps(bill_dict)
        qs = bills
        cols = ['id', 'created', 'who_paid', 'quantity_paid', 'who_owes__member']
        df = read_frame(qs, cols, verbose=True)
        bills = df.to_json(orient='records')
        data['bills'] = bills
        data['lah'] = bill_dict


        qs = payments
        df = read_frame(qs)
        payments = df.to_json(orient='records')
        data['payments'] = payments

    return render(request, template_name, data)


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()
