from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.payments_list, name='payments_list'),
    url(r'^new$', views.payments_create, name='payments_new'),
    url(r'^(?P<pk>\d+)/$', views.payments_read, name='payments_read'),
    url(r'^edit/(?P<pk>\d+)$', views.payments_update, name='payments_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.payments_delete, name='payments_delete'),
    ]