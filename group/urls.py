from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.group_list, name='group_list'),
    url(r'^new$', views.group_create, name='group_new'),
    url(r'^(?P<pk>\d+)/$', views.group_read, name='group_read'),
    url(r'^find$', views.group_find, name='group_find'),
    url(r'^edit/(?P<pk>\d+)$', views.group_update, name='group_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.group_delete, name='group_delete'),
    url(r'^(?P<pk>\d+)/members/$', views.group_manage_members, name='group_manage_members'),
    url(r'^(?P<pk>\d+)/members/delete/(?P<id>\d+)$', views.group_member_delete,
        name='group_member_delete'),
    url(r'^set_group/(?P<pk>\d+)$', views.set_current_group, name='set_current_group'),
    ]