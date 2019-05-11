from django.contrib import admin 
from main.models import NoticeBoard
from main.models import chk_value
from main.models import Profile

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name']


admin.site.register(NoticeBoard,NoticeAdmin)	# admin site에 model class 가져오기

class chk_valueAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']

admin.site.register(chk_value, chk_valueAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id','nickname']

admin.site.register(Profile, ProfileAdmin)


# from django.contrib.auth.models import User 
# from django.contrib.auth.admin import UserAdmin 
# from project.app.models import UserProfile 

# admin.site.unregister(User) 

# class UserProfileInline(admin.StackedInline): 
# 	model = UserProfile 

# class UserProfileAdmin(UserAdmin): 
# 	inlines = [UserProfileInline] 
# 	admin.site.register(User, UserProfileAdmin)
