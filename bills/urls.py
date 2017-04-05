from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.bills_list, name='bills_list'),
    url(r'^new$', views.bills_create, name='bills_new'),
    url(r'^(?P<pk>\d+)/$', views.bills_read, name='bills_read'),
    url(r'^edit/(?P<pk>\d+)$', views.bills_update, name='bills_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.bills_delete, name='bills_delete'),

    ]