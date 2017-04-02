from django import forms
from bills.models import Household


class RegisterHousemateForm(forms.ModelForm):
    name = forms.CharField(label="name", widget=forms.TextInput(attrs={'placeholder': "Household Name"}), required=True)
    password = forms.CharField(label="password", widget=forms.TextInput(attrs={'placeholder': "Household Password"}), required=True)

    class Meta:
        model = Household
        fields = ('name','password',)

    def clean_name(self):
        """
        Ensure the name and password match
        """
        name = self.cleaned_data.get("name")
        qs = Household.objects.filter(name=name).count()
        if qs == 0:
            return name
        raise forms.ValidationError(("That household name is already taken!"))
