from django import forms
from django.forms import ModelForm

from .models import Household


class HouseholdForm(ModelForm):

    class Meta:
        model = Household
        fields = ['name', 'password']

class EnterHouseholdForm(forms.Form):
    name = forms.CharField(label="name", required=True)
    password = forms.CharField(label="password", required=True)

    class Meta:
        # model = Household
        fields = ('name','password',)

    def clean_password(self):
        """
        Ensure the name and password match
        """
        name = self.cleaned_data.get("name")
        pw = self.cleaned_data.get("password")
        qs = Household.objects.filter(name=name).count()
        if qs == 0:
            forms.ValidationError(("That household doesn't exist!"))
        for household in Household.objects.filter(name=name):
            if pw == household.password:
                print("Match!")

            else:
                print("Wrong Password!")
                raise forms.ValidationError(("That doesn't seem correct. Please try again."))


