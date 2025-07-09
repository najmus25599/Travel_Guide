from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'bus'

urlpatterns = [
    url(r'^$', views.bus_search, name="Buses"),
    url(r'^(?P<slug>[\w-]+)/$',views.view_bus),
    url(r'^(?P<slug>[\w-]+)/token/$', views.ticket_pdf, name="Token"),
]