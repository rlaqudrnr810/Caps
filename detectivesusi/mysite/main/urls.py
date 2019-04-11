from django.urls import path
from . import views	# 현재 폴더 views import

app_name='main'
urlpatterns = [
	path('', views.index,name='home'),
	path('about/', views.about,name='about'),
	path('contact/', views.contact,name='contact'),
	path('login/', views.login, name='login'),
	path('mypage/', views.mypage, name='mypage'),
	path('result/', views.result, name='result'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    #path('search/', views.search, name='search'),
    path('search/', views.search, name='search'),
    path('searchWork/', views.searchWork, name='search'),
    path('faq/', views.faq, name='faq'),

    # board
    path('notice/', views.notice, name='notice'),
    path('show_write_form/', views.show_write_form),
    path('DoWriteBoard/', views.DoWriteBoard),
    path('listSpecificPageWork/', views.listSpecificPageWork),
    path('viewWork/', views.viewWork),
    path('listSpecificPageWork_to_update/', views.listSpecificPageWork_to_update),
    path('updateBoard/', views.updateBoard),
    path('DeleteSpecificRow/', views.DeleteSpecificRow),
   # path('listSpecificPageWork/$', views.listSpecificPageWork),
	#path('^areas/(?P<area>.+)/$', views.areas),
]
