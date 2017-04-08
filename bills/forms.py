from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from bills.models import Bill


class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ['who_paid', 'description', 'quantity_paid', 'household']

    def __init__(self, test, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        # if "instance" in kwargs and kwargs["instance"] is not None:
        #     product = kwargs["instance"].product
        #     qs = self.fields["image"].queryset.filter(product=product)
        #     self.fields["image"].queryset = qs
        # else:
        #     self.fields["image"].queryset = self.fields["image"].queryset.none()
