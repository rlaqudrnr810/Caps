from django.shortcuts import render
from django.http import HttpResponse
from .models import Candidate , Poll, Choice

import datetime

def index(request):
	candidates = Candidate.objects.all() #Candidate에 있는 row 불러옴
	context = {'candidates':candidates}
	return render(request, 'elections/index.html',context)

def areas(request, area) : #어떤 지역인지를 매개변수 area로 받습니다.
    today = datetime.datetime.now()
    try :
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte=today) # get에 인자로 조건을 전달해줍니다. 
        candidates = Candidate.objects.filter(area = area) # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates,
    'area' : area}
    return render(request, 'elections/area.html', context)
