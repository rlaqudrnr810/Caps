from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),		# 빈 url -> main.urls 참고 -> index.html 표시
]
