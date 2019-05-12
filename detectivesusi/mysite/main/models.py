from django.db import models
from django.contrib.auth.models import User 		#django user model

# user model extension
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10,default='SOME STRING')# 이름
    sex = models.CharField(max_length=10,default='SOME STRING')		# 성별
    age = models.CharField(max_length=10,default='SOME STRING')		# 나이
    phonenum = models.CharField(max_length=10,default='SOME STRING')# 핸드폰번호
    area = models.CharField(max_length=10,default='SOME STRING')	# 사는지역
    h_type = models.CharField(max_length=10,default='SOME STRING')	# 고등학교 유형
####

# notice board
class NoticeBoard(models.Model):
															#글번호 자동생성(pk)
	subject = models.CharField(max_length=50,blank=True)	#제목
	name = models.CharField(max_length=50,blank=True)		#이름
	created_date = models.DateField(null=True, blank=True)	#생성일
	memo = models.TextField(max_length=1000, blank=True)	#내용
	hits = models.IntegerField(null=True,blank=True)		#조회수

# search page 데이터 입력
class chk_value(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)		#user
	preferwhere1 = models.CharField(null=True,blank=True,max_length=50)	#선호지역
	preferwhere2 = models.CharField(null=True,blank=True,max_length=50)
	preferwhere3 = models.CharField(null=True,blank=True,max_length=50)
	prefertype1 = models.CharField(null=True,blank=True,max_length=50)		#선호계열
	prefertype2 = models.CharField(null=True,blank=True,max_length=50)
	prefertype3 = models.CharField(null=True,blank=True,max_length=50)
	prefertype4 = models.CharField(null=True,blank=True,max_length=50)
	prefertype5 = models.CharField(null=True,blank=True,max_length=50)
	prefertype6 = models.CharField(null=True,blank=True,max_length=50)
	total_avgrate = models.FloatField(null=True,blank=True)		#평균 내신
	main_avgrate = models.FloatField(null=True,blank=True)		#주요과목 내신
	executive_cnt = models.IntegerField(null=True,blank=True)	#임원활동
	absent = models.IntegerField(null=True,blank=True)			#무단결석
	award_cnt = models.IntegerField(null=True,blank=True)		#수상경력
	circle_cnt = models.IntegerField(null=True,blank=True)		#동아리활동
	volunteer = models.IntegerField(null=True,blank=True)		#봉사시간
	reading = models.IntegerField(null=True,blank=True)			#독후감

# mypage 학년 별 데이터 입력
class input_data(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)	# user
	grade = models.IntegerField(null=True,blank=True)		# 학년,학기 11,12,21,22,31,32
	subject1 = models.CharField(null=True,blank=True,max_length=50)	# 교과
	subject2 = models.CharField(null=True,blank=True,max_length=50) # 과목
	complete_unit = models.IntegerField(null=True,blank=True)		# 이수단위
	rate = models.FloatField(null=True,blank=True)		# 취득한 등급

class c_admission(models.Model):
	c_name = models.CharField(null=True,blank=True,max_length=50)	# 대학교 이름
	d_name = models.CharField(null=True,blank=True,max_length=50)	# 학과 이름
	admission = models.CharField(null=True,blank=True,max_length=50)# 전형명
	year = models.IntegerField(null=True,blank=True)				# 연도
	cut_off = models.FloatField(null=True,blank=True)				# 주요과목 내신
	ad_info = models.CharField(null=True,blank=True,max_length=50)	# 입학 정보