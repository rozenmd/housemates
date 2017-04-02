from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.admin.views.decorators import staff_member_required
from household.models import Household, HouseholdMember
from .forms import EnterHouseholdForm


class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = ['name', 'password']


def household_list(request, template_name='household/household_list.html'):
    households = Household.objects.all()
    data = {}
    data['object_list'] = households
    return render(request, template_name, data)


def household_create(request, template_name='household/household_form.html'):
    form = HouseholdForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('household_list')
    return render(request, template_name, {'form': form})


def household_read(request, pk, template_name='household/household_view.html'):
    household = get_object_or_404(Household, pk=pk)
    household_name = household.name
    form = EnterHouseholdForm(request.POST or None,initial={'name': household_name})
    form.name = household_name
    if form.is_valid():
        print("Adding user to Household")
        user = request.user
        HouseholdMember(member=user,household=household).save()
        return redirect('household_list')

    return render(request, template_name, {'household_name': household_name, 'form':form})



def household_update(request, pk, template_name='household/household_form.html'):
    household = get_object_or_404(Household, pk=pk)
    form = HouseholdForm(request.POST or None, instance=household)
    if form.is_valid():
        form.save()
        return redirect('household_list')
    return render(request, template_name, {'form': form})

@staff_member_required
def household_delete(request, pk, template_name='household/household_confirm_delete.html'):
    household = get_object_or_404(Household, pk=pk)
    if request.method == 'POST':
        household.delete()
        return redirect('household_list')
    return render(request, template_name, {'object': household})
