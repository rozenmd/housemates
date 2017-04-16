from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from bills.models import Bill
from group.models import GroupMember, Group
from bills.forms import BillForm
from web.models import MyProfile

# Create your views here.


def bills_list(request, template_name='bills/bills_list.html'):
    groups = Group.objects.filter(group_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group.id)
    else:
        current_group = ''
    data = {'current_group': current_group}

    match = GroupMember.objects.filter(member=request.user)
    if match:
        bills = Bill.objects.filter(group=current_group)

        data['object_list'] = bills
        return render(request, template_name, data)
    else:
        return HttpResponse("""
        <h1>You need to join or create a group!</h1>
        <button onclick="goBack()">Go Back</button>
        
        <script>
        function goBack() {
            window.history.back();
        }
        </script>
        """)



def bills_create(request, template_name='bills/bills_form.html'):
    groups = Group.objects.filter(group_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    data = {'current_group': current_group}
    match = GroupMember.objects.filter(member=request.user)
    if match:
        bills = Bill.objects.filter(group=current_group)
        data['object_list'] = bills

    form = BillForm(request.POST or None, initial={'group': current_group})
    form.fields['who_paid'].queryset = GroupMember.objects.filter(group=current_group)
    form.fields['who_owes'].queryset = GroupMember.objects.filter(group=current_group)
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
