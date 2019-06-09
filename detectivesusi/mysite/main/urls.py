from django.urls import path
from . import views	# 현재 폴더 views import
from django.conf.urls import handler404, handler500

from django.conf import settings
from django.conf.urls.static import static
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
 
    path('search/', views.search, name='search'),
    path('searchWork/', views.searchWork, name='search'),
    path('search_result/', views.search_result),
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
    path('idcheck/', views.idcheck),
    # save in search page
    path('save_chk/', views.save_chk),
    path('save_chk2/', views.save_chk2),
    path('save_chk1/', views.save_chk1),
    path('prev_result_del/',views.del_result),
    path('show_result/',views.show_result),

    # 점수 등록
    path('mypage/igradeWork/',views.igrade1),
    # 점수 삭제
    path('igrade_del/',views.igrade_del),

    path('hap/',views.hap),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# handler404 = 'main.views.handler404'
# handler500 = 'main.views.hander500'