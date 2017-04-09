from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from group.models import Group
from web.models import MyProfile


def dashboard(request, template_name='web/dashboard.html'):
    profile = MyProfile.objects.filter(user=request.user)
    if len(profile) > 0:
        current_group = get_object_or_404(Group, pk=profile.first().current_group)
    else:
        current_group = ''
    data = {'current_group': current_group}
    return render(request, template_name, data)
