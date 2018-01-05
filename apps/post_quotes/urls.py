from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^quotes$', views.quotes),
    url(r'^log_out$', views.log_out),
    url(r'^create$', views.create),
    url(r'^add/(?P<quote_id>\d+)$', views.add),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^delete/(?P<quote_id>\d+)$', views.delete),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    
]