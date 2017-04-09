
from django.forms import ModelForm
from django import forms
from payments.models import Payment
from group.models import GroupMember


class PaymentForm(ModelForm):
    # group = forms.CharField(label="Household", required=True,disabled=True)
    # description = forms.CharField(label="Description", required=False)
    class Meta:
        model = Payment
        fields = ['from_user', 'to_user', 'group','quantity_paid']
