from django.db import models

class NoticeBoard(models.Model):
															#글번호 자동생성(pk)
	subject = models.CharField(max_length=50,blank=True)	#제목
	name = models.CharField(max_length=50,blank=True)		#이름
	created_date = models.DateField(null=True, blank=True)	#생성일
	memo = models.CharField(max_length=1000, blank=True)	#내용
	hits = models.IntegerField(null=True,blank=True)		#조회수

