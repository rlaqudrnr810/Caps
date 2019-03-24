from django.conf.urls import url
from . import views

app_name='elections'
urlpatterns = [
	url(r'^$', views.index,name='home'),
	url(r'^areas/(?P<area>.+)/$', views.areas),
]
