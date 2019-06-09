from django.contrib import admin 
from main.models import NoticeBoard
from main.models import chk_value
from main.models import Profile
from main.models import input_data
from main.models import c_admission
from main.models import c_info
from main.models import p_case
from main.models import search_history

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name']


admin.site.register(NoticeBoard,NoticeAdmin)	# admin site에 model class 가져오기

class chk_valueAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']

admin.site.register(chk_value, chk_valueAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id','nickname']

admin.site.register(Profile, ProfileAdmin)

class input_dataAdmin(admin.ModelAdmin):
    list_display = ['user', 'grade','subject1','subject2','complete_unit','rate']
admin.site.register(input_data, input_dataAdmin)

class c_admissionAdmin(admin.ModelAdmin):
    list_display = ['c_name','d_name','year']
admin.site.register(c_admission, c_admissionAdmin)

class c_infoAdmin(admin.ModelAdmin):
    list_display = ['c_name', 'area']
admin.site.register(c_info, c_infoAdmin)

class p_caseAdmin(admin.ModelAdmin):
    list_display = ['c_name', 'id']
admin.site.register(p_case, p_caseAdmin)

class search_historyAdmin(admin.ModelAdmin):
    list_display = ['ch_val', 'c_name']
admin.site.register(search_history, search_historyAdmin)