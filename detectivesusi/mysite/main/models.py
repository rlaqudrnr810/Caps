from django.db import models
from django.contrib.auth.models import User 		#django user model

class NoticeBoard(models.Model):
															#글번호 자동생성(pk)
	subject = models.CharField(max_length=50,blank=True)	#제목
	name = models.CharField(max_length=50,blank=True)		#이름
	created_date = models.DateField(null=True, blank=True)	#생성일
	memo = models.TextField(max_length=1000, blank=True)	#내용
	hits = models.IntegerField(null=True,blank=True)		#조회수


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
