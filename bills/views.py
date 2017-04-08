from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.admin.views.decorators import staff_member_required
from bills.models import Bill, Payment
from household.models import HouseholdMember, Household
from bills.forms import BillForm


# Create your views here.

class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ['who_paid', 'description', 'quantity_paid', 'household']

    def __init__(self, test, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        # if "instance" in kwargs and kwargs["instance"] is not None:
        #     product = kwargs["instance"].product
        #     qs = self.fields["image"].queryset.filter(product=product)
        #     self.fields["image"].queryset = qs
        # else:
        #     self.fields["image"].queryset = self.fields["image"].queryset.none()


def bills_list(request, template_name='bills/bills_list.html'):
    current_user = request.user
    match = HouseholdMember.objects.filter(member=current_user)
    if match:
        bills = Bill.objects.all()
        data = {}
        data['object_list'] = bills
        return render(request, template_name, data)
    else:
        return HttpResponse("""
        <h1>You need to join or create a household!</h1>
        <button onclick="goBack()">Go Back</button>
        
        <script>
        function goBack() {
            window.history.back();
        }
        </script>
        """)



def bills_create(request, template_name='bills/bills_form.html'):
    form = BillForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('bills_list')
    return render(request, template_name, {'form': form})


def bills_read(request, pk, template_name='bills/bills_view.html'):
    bills = get_object_or_404(Bill, pk=pk)
    form = BillForm(request.POST or None, instance=bills)
    if form.is_valid():
        form.save()
        return redirect('bills_list')
    return render(request, template_name, {'form': form})


def bills_update(request, pk, template_name='bills/bills_form.html'):
    bills = get_object_or_404(Bill, pk=pk)
    form = BillForm(request.POST or None, instance=bills)
    if form.is_valid():
        form.save()
        return redirect('bills_list')
    return render(request, template_name, {'form': form})


def bills_delete(request, pk, template_name='bills/bills_confirm_delete.html'):
    bills = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        bills.delete()
        return redirect('bills_list')
    return render(request, template_name, {'object': bills})
