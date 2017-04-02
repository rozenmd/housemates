from django import forms
from .models import Household


class EnterHouseholdForm(forms.Form):
    name = forms.CharField(label="name", widget=forms.TextInput(attrs={'placeholder': "Household Name"}), required=False, disabled=True)
    password = forms.CharField(label="password", widget=forms.TextInput(attrs={'placeholder': "Household Password"}), required=True)

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
