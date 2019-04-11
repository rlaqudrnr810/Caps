from django.contrib import admin 
from main.models import NoticeBoard

admin.site.register(NoticeBoard)	# admin site에 model class 가져오기

# from django.contrib.auth.models import User 
# from django.contrib.auth.admin import UserAdmin 
# from project.app.models import UserProfile 

# admin.site.unregister(User) 

# class UserProfileInline(admin.StackedInline): 
# 	model = UserProfile 

# class UserProfileAdmin(UserAdmin): 
# 	inlines = [UserProfileInline] 
# 	admin.site.register(User, UserProfileAdmin)
