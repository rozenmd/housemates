from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.admin.views.decorators import staff_member_required
from bills.models import Bill, Payment
from household.models import HouseholdMember, Household
from bills.forms import BillForm
from web.models import MyProfile

# Create your views here.


def bills_list(request, template_name='bills/bills_list.html'):
    households = Household.objects.filter(household_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_household = get_object_or_404(Household, pk=profile.first().current_household)
    else:
        current_household = ''
    data = {'current_household': current_household}

    match = HouseholdMember.objects.filter(member=request.user)
    if match:
        bills = Bill.objects.filter(household=current_household)

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
    households = Household.objects.filter(household_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_household = get_object_or_404(Household, pk=profile.first().current_household)
    else:
        current_household = ''
    data = {'current_household': current_household}
    match = HouseholdMember.objects.filter(member=request.user)
    if match:
        bills = Bill.objects.filter(household=current_household)
        data['object_list'] = bills

    form = BillForm(request.POST or None, initial={'household': current_household})
    form.fields['who_paid'].queryset = HouseholdMember.objects.filter(household=current_household)
    form.fields['who_owes'].queryset = HouseholdMember.objects.filter(household=current_household)
    if form.is_valid():
        form.save()
        return redirect('bills_list')
    data['form'] = form
    return render(request, template_name, data)


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
