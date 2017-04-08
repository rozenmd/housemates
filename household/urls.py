from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.household_list, name='household_list'),
    url(r'^new$', views.household_create, name='household_new'),
    url(r'^(?P<pk>\d+)/$', views.household_read, name='household_read'),
    url(r'^find$', views.household_find, name='household_find'),
    url(r'^edit/(?P<pk>\d+)$', views.household_update, name='household_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.household_delete, name='household_delete'),
    url(r'^(?P<pk>\d+)/members/$', views.household_manage_members, name='household_manage_members'),
    url(r'^(?P<pk>\d+)/members/delete/(?P<id>\d+)$', views.household_member_delete,
        name='household_member_delete'),
    url(r'^set_household/(?P<pk>\d+)$', views.set_current_household, name='set_current_household'),
    ]