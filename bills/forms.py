
from django.forms import ModelForm
from django import forms
from bills.models import Bill
from group.models import GroupMember


class BillForm(ModelForm):
    # group = forms.CharField(label="Household", required=True,disabled=True)
    # description = forms.CharField(label="Description", required=False)
    class Meta:
        model = Bill
        fields = ['who_paid', 'description', 'quantity_paid','who_owes','group']
