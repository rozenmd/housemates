from django.forms import ModelForm
from django import forms
from bills.models import Bill
from group.models import GroupMember


class BillForm(ModelForm):
    # group = forms.CharField(label="Household", required=True,disabled=True)
    who_paid = forms.ModelChoiceField(required=True, queryset="",
                                      widget=forms.Select(attrs={'class': 'col-sm-12 col-xs-12'}))
    who_owes = forms.ModelChoiceField(required=True, queryset="",
                                      widget=forms.Select(attrs={'class': 'col-sm-12 col-xs-12'}))
    description = forms.CharField(label="Description", required=False,
                                  widget=forms.Textarea(attrs={'style': 'height:75px', 'class': 'col-sm-12 col-xs-12'}))
    quantity_paid = forms.DecimalField(label="Quantity Paid", required=True,
                                       widget=forms.NumberInput(attrs={'class': 'col-sm-12 col-xs-12'}))

    class Meta:
        model = Bill
        fields = ['who_paid', 'description', 'quantity_paid', 'who_owes', 'group']
