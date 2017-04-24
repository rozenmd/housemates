
from django.forms import ModelForm
from django import forms
from payments.models import Payment
from group.models import GroupMember


class PaymentForm(ModelForm):
    from_user = forms.ModelChoiceField(required=True, queryset="",
                                      widget=forms.Select(attrs={'class': 'col-sm-12 col-xs-12'}))
    to_user = forms.ModelChoiceField(required=True, queryset="",
                                      widget=forms.Select(attrs={'class': 'col-sm-12 col-xs-12'}))
    quantity_paid = forms.DecimalField(label="Quantity Paid", required=True,
                                       widget=forms.NumberInput(attrs={'class': 'col-sm-12 col-xs-12'}))
    class Meta:
        model = Payment
        fields = ['from_user', 'to_user', 'group','quantity_paid']
