from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.household_list, name='household_list'),
    url(r'^new$', views.household_create, name='household_new'),
    url(r'^(?P<pk>\d+)/$', views.household_read, name='household_read'),
    url(r'^edit/(?P<pk>\d+)$', views.household_update, name='household_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.household_delete, name='household_delete'),
    ]