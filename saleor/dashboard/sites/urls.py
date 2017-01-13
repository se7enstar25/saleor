from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='site-index'),
    url(r'^add/$', views.create, name='site-create'),
    url(r'^(?P<site_id>[0-9]+)/edit/$', views.update, name='site-update'),
    url(r'^(?P<site_id>[0-9]+)/delete/$', views.delete, name='site-delete'),
]
