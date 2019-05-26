from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),		# 빈 url -> main.urls 참고 -> index.html 표시
]

handler404 = 'main.views.handler404'
handler500 = 'main.views.hander500'