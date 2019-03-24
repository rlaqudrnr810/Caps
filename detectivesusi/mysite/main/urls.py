from django.urls import path
from . import views	# 현재 폴더 views import

app_name='main'
urlpatterns = [
	path('', views.index,name='home'),
	path('about/', views.about,name='about'),
	path('contact/', views.contact,name='contact'),
	path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
	#path('^areas/(?P<area>.+)/$', views.areas),
]
