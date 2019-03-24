from django.db import models

# Create your models here.
class Candidate(models.Model):	# Candidate Model 정의 (상속)
	name = models.CharField(max_length=10)	# 최대길이 10
	introduction = models.TextField()		# 길이제한없이 텍스트
	area = models.CharField(max_length=15)	# 지역
	party_number = models.IntegerField(default=0)

	def __str__(self):			# 후보자의 이름으로 표현
								# object를 표현하는 문자열을 정의할 때는 __str__메소드를 오버라이딩
		return self.name

class Poll(models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	area = models.CharField(max_length=15)

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	candidate = models.ForeignKey(Candidate)
	votes=models.IntegerField(default=0)
