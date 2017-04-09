from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.admin.views.decorators import staff_member_required
from group.models import Group, GroupMember
from .forms import EnterGroupForm, GroupForm
from django.contrib import messages
from web.models import MyProfile


def group_list(request, template_name='group/group_list.html'):
    groups = Group.objects.filter(group_member__member=request.user)
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    data = {'object_list': groups, 'current_group': current_group}
    return render(request, template_name, data)


def group_create(request, template_name='group/group_form.html'):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        group = form.save()
        GroupMember(member=request.user, group=group).save()
        return redirect('group_list')
    return render(request, template_name, {'form': form})


def group_read(request, pk, template_name='group/group_view.html'):
    group = get_object_or_404(Group, pk=pk)
    current_user = request.user
    match = GroupMember.objects.filter(member=current_user, group=group)
    if match:
        #Send them through
        return redirect('group_manage_members', group.id)
    group_name = group.name
    form = EnterGroupForm(request.POST or None, initial={'name': group_name})
    if form.is_valid():
        print("Adding user to Group")
        GroupMember(member=current_user, group=group).save()
        return redirect('group_list')

    return render(request, template_name, {'group_name': group_name, 'form':form})


def group_find(request, template_name='group/group_find.html'):
    current_user = request.user
    form = EnterGroupForm(request.POST or None)
    if form.is_valid():
        print("Adding user to Group")
        house = Group.objects.get(name=form.cleaned_data['name'])
        GroupMember(member=current_user, group=house).save()
        return redirect('group_list')

    return render(request, template_name, {'form':form})


def group_update(request, pk, template_name='group/group_form.html'):
    group = get_object_or_404(Group, pk=pk)
    current_user = request.user
    match = GroupMember.objects.filter(member=current_user, group=group)
    if not match:
        raise Http404
    form = GroupForm(request.POST or None, instance=group)
    if form.is_valid():
        form.save()
        return redirect('group_list')
    return render(request, template_name, {'form': form})


@staff_member_required
def group_delete(request, pk, template_name='group/group_confirm_delete.html'):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, template_name, {'object': group})


@staff_member_required
def group_member_delete(request, pk, id, template_name='group/group_member_confirm_delete.html'):
    group = get_object_or_404(Group, pk=pk)
    member = get_object_or_404(GroupMember, pk=id)
    if request.method == 'POST':
        member.delete()
        return redirect('group_manage_members', group.id)
    return render(request, template_name, {'object': member})


def group_manage_members(request, pk, template_name='group/group_member_list.html'):
    current_user = request.user
    context = {}
    group = get_object_or_404(Group, pk=pk)
    match = GroupMember.objects.filter(member=current_user, group=group)
    if match.count() > 0:
        # Then the groupMember is in our house
        members = GroupMember.objects.filter(group=group)
        data = {'object_list': members}
        return render(request, template_name, data)
    else:
        return redirect('group_list')

def set_current_group(request, pk):
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        profile = MyProfile.objects.get(user=request.user)
        profile.current_group = pk
        profile.save()
    else:
        MyProfile(user=request.user, current_group=pk).save()
    messages.add_message(request, messages.INFO, 'Current group updated!')

    return redirect('group_list')
