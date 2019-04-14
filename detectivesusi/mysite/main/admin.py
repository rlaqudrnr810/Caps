from django.contrib import admin 
from main.models import NoticeBoard
from main.models import chk_value

admin.site.register(NoticeBoard)	# admin site에 model class 가져오기
admin.site.register(chk_value)	# admin site에 model class 가져오기
# from django.contrib.auth.models import User 
# from django.contrib.auth.admin import UserAdmin 
# from project.app.models import UserProfile 

# admin.site.unregister(User) 

# class UserProfileInline(admin.StackedInline): 
# 	model = UserProfile 

# class UserProfileAdmin(UserAdmin): 
# 	inlines = [UserProfileInline] 
# 	admin.site.register(User, UserProfileAdmin)
