from django.shortcuts import get_object_or_404
from django.db.models import F

import time
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from .forms import LoginForm, SignupForm
from .models import NoticeBoard
from .models import chk_value
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.db.models import Q
from .models import Profile
from .models import search_history
from .models import c_admission
from .models import input_data
from .models import p_case

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def search_result(request):
    #현재유저 정보 user 에 저장
    # 검색 결과 insert
    # __gt = 값 : 값보다 큰 값 필터됨 .
    # __lt = 값 : 값보다 작은 값 필터됨.
    # Entry.objects.get(조건) : 하나의 데이터 얻어옴
    # model1.objects.filter(name__contains=’com’) com 포함한 문자열 필터
    # Blog 모델의 이름이 Beatles Blog인 데이터과 관계있는 Entry 객체 반환
    # >>> Entry.objects.filter(blog__name='Beatles Blog')
    # h_cut_off : 가장 좋은 성적
    # cut_off : 평균 성적
    # l_cut_off : 가장 낮은 성적

    user = request.user
    postset = chk_value.objects.filter(user=user).order_by('-pk')[0]

    # 소신 대학리스트 뽑기      합격자 가장 좋은 내신 =  본인내신-0.2 ~ 본인내신-0.5
    if search_history.objects.filter(ch_val=postset).count()==0:    #0임
        if Profile.objects.get(user=user).h_type=="특성화": 
            unsafe_outputList = c_admission.objects.filter(l_cut_off__lt=2*postset.total_avgrate-F('cut_off'),l_cut_off__gt=postset.total_avgrate).filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6))
        else:   #특성화 고교 아닐 시 특성화 아닌 result set
            unsafe_outputList = c_admission.objects.filter(l_cut_off__lt=2*postset.total_avgrate-F('cut_off'),l_cut_off__gt=postset.total_avgrate).filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6)).filter(~Q(admission__contains="특성화"))#, l_cut_off__lt=2*postset.total_avgrate-F('cut_off'))
        #unsafe_outputList= unsafe_outputList.filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6)).order_by('?')[:4]
        if Profile.objects.get(user=user).sex=="남":
            unsafe_outputList = unsafe_outputList.filter(~Q(c_name__contains="여자")).order_by('?')[:4]
        else:
            unsafe_outputList = unsafe_outputList.order_by('?')[:4]
        for s in unsafe_outputList:    # 소신 대학 리스트
            search_his = search_history (ch_val=postset,
                                        c_name=s,
                                        r_type="소신"
                                        )
            search_his.save()


        # 적정 대학리스트 뽑기
        if Profile.objects.get(user=user).h_type=="특성화": 
            outputList = c_admission.objects.filter(l_cut_off__gt=2*postset.total_avgrate-F('cut_off'),  h_cut_off__lt=2*postset.total_avgrate-F('cut_off')).filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6))
        else:
            outputList = c_admission.objects.filter(l_cut_off__gt=2*postset.total_avgrate-F('cut_off'),  h_cut_off__lt=2*postset.total_avgrate-F('cut_off')).filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6)).filter(~Q(admission__contains="특성화"))

        if Profile.objects.get(user=user).sex=="남":
            outputList = outputList.filter(~Q(c_name__contains="여자")).order_by('?')[:4]
        else:
            outputList = outputList.order_by('?')[:4]

        for s in outputList:    # 적정 대학 리스트
            search_his = search_history (ch_val=postset,
                                        c_name=s,
                                        r_type="적정"
                                        )
            search_his.save()
        
        # 안정 대학 리스트 뽑기
        if Profile.objects.get(user=user).h_type=="특성화": 
            safe_outputList = c_admission.objects.filter(h_cut_off__gt=2*postset.total_avgrate-F('cut_off'),h_cut_off__lt=postset.total_avgrate).filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6))
        else:
            safe_outputList = c_admission.objects.filter(h_cut_off__gt=2*postset.total_avgrate-F('cut_off'),h_cut_off__lt=postset.total_avgrate).filter(Q(d_name__contains=postset.prefertype1)|Q(d_name__contains=postset.prefertype2)|Q(d_name__contains=postset.prefertype3)|Q(d_name__contains=postset.prefertype4)|Q(d_name__contains=postset.prefertype5)|Q(d_name__contains=postset.prefertype6)).filter(~Q(admission__contains="특성화"))

        if Profile.objects.get(user=user).sex=="남":
            safe_outputList = safe_outputList.filter(~Q(c_name__contains="여자")).order_by('?')[:4]
        else:
            safe_outputList = safe_outputList.order_by('?')[:4]

        for s in safe_outputList:    # 안정 대학 리스트
            search_his = search_history (ch_val=postset,
                                        c_name=s,
                                        r_type="안정"
                                        )
            search_his.save()
        time.sleep(3)
        context = {
                'uso_list':unsafe_outputList,
                'o_list':outputList,
                'so_list':safe_outputList,
                }
        #messages.success(request,"분석 완료 이동합니다.")
        return render(request, 'main/search_result.html',context)
    else:   # 에러
        return render(request, 'main/index.html')

    # 계산항목 #
    # where d_name like %chk_val.prefertype1% || # preferwhere1, preferwhere2, preferwhere3 => univ where
    # prefertype1, prefertype2, prefertype3, prefertype4, prefertype5, prefertype6 => prefertype
    # total_avgrate, main_avgrate, executive_cnt, absent, award_cnt, circle_cnt, volunteer, reading

#mypage (성적입력)
def mypage(request):
    user=request.user
    igrade = request.GET['igrade']
    input_rs = input_data.objects.filter(user=user).filter(grade=igrade)
    context = {
        'igrade':igrade,
        'input_rs':input_rs,
    }
    return render(request,'main/mypage.html',context)

@csrf_exempt
def igrade1(request):
    if 'rcount' in  request.POST:
        rcount = request.POST['rcount']
    else:
        rcount = False
    
    igrade=request.GET['igrade']
    
    # 성적 추가하기
    for j in range(1,int(rcount)+1):
        idate = input_data (
                     user = request.user,
                     grade= igrade, 
                     subject1 = request.POST['cmpl-'+str(j)],
                     subject2 = request.POST['sbject-'+str(j)],
                     complete_unit = request.POST['unit-'+str(j)],
                     rate = request.POST.get('grde-'+str(j),False),
            )
        idate.save()
    
    url = '../?igrade='+igrade
    
    return redirect(url)

def hap(request):
    id = request.GET['id']
    col=c_admission.objects.get(id=id)
    p = p_case.objects.filter(c_name__c_name=col.c_name)
    context = {
            'p' : p,
    }
    return render(request, 'main/hap.html',context)

# 성적 삭제하기.
def igrade_del(request):
    igrade = request.GET['igrade']
    rid=request.GET['id']
    user=request.user
    p=input_data.objects.get(id=rid)
    p.delete()
    url='../mypage/?igrade='+igrade
    return redirect(url)

# prev. result
def result(request):
    user = request.user
    datas = chk_value.objects.filter(user=user).order_by('-created_date')   # date 최신것 부터 목록뽑기
    context = {
        'chk_value':datas
    }
    return render(request,'main/result.html',context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
	return render(request, 'main/contact.html')

def search(request):
    user=request.user
    if user.is_authenticated:
        datass = input_data.objects.filter(user=user)
        context = {
            'input_datas': datass,
        }
        return render(request, 'main/search.html',context)
    return render(request, 'main/search.html')    

def faq(request):
	return render(request, 'main/faq.html')

# login & sign up #
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(
                username=username,
                password=password
            )

            if user:
                django_login(request, user)
                return redirect('main:home')
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'main/login.html', context)

def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
           # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
        if signup_form.is_valid():
        	  # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
            user=signup_form.signup()

            nickname = request.POST["nickname"]
            type = request.POST["type"]
            sex=request.POST["sex"]
            h_type=request.POST["h_type"]
            profile = Profile(user=user, nickname=nickname,type=type,sex=sex,h_type=h_type)
            profile.save()
            django_login(request, user)
            #auth.login(request,user) #로그인 유지
            #return redirect('main:home')
            return render(request,'main/index.html',{'some_flag':True})
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'main/signup.html', context)

def logout(request):
    django_logout(request)
    return redirect('main:home')

#########################################################################################

# Notice board section #
rowsPerPage = 5
def notice(request):
    #OK
    #url = '/listSpecificPageWork?current_page=1'
    # return HttpResponseRedirec(url)
    boardList = NoticeBoard.objects.order_by('id')[0:5]
    current_page =1
    totalCnt = NoticeBoard.objects.all().count()

    pagingHelperIns = pagingHelper()    #객체 생성
    totalPageList = pagingHelperIns.getTotalPageList(totalCnt,rowsPerPage)
    print ('totalPageList',totalPageList)
    context = {
        'boardList':boardList,
        'totalCnt':totalCnt,
        'current_page':current_page,
        'totalPageList':totalPageList,
    }
    return render(request,'main/listSpecificPage.html',context)
    # render_to_response() 함수 첫번 째 매개변수에 템플릿 파일명을 적어준다.
    #두번째 매개변수에는 넘겨줄 데이터를 적어준다.
class pagingHelper:
    def getTotalPageList(self, total_cnt,rowsPerPage):
        if((total_cnt % rowsPerPage)==0):
            self.total_pages=int(total_cnt/rowsPerPage)
            print ('getTotalPageList #1')
        else:
            self.total_pages=int((total_cnt/rowsPerPage)+1)
            print ('getTotalPageList #2')

        self.totalPageList=[]
        for j in range(self.total_pages):
            self.totalPageList.append(j+1)
        return self.totalPageList

    def __init__(self):
        self.total_pages=0
        self.totalPageList=0

@csrf_exempt #post로 값을 전송시 CSRF 보안 목적으로 추가
def DoWriteBoard(request):
    br = NoticeBoard (subject = request.POST['subject'],
                      name = request.POST['name'],
                      memo = request.POST['memo'],
                      created_date = timezone.now(),
                      hits = 0
                     )
    br.save()   

    # 저장을 했으니, 다시 조회해서 보여준다.
    url = '/listSpecificPageWork?current_page=1'
    return redirect(url)

def listSpecificPageWork(request):
    current_page = request.GET['current_page']
    totalCnt = NoticeBoard.objects.all().count()

    print ('current_page=', current_page)

    # 페이지를 가지고 범위 데이터를 조회한다 => raw SQL 사용함
    boardList = NoticeBoard.objects.raw('SELECT * FROM MAIN_NOTICEBOARD')
    # Raw query must include the primary key

    # boardList = NoticeBoard.objects.raw('SELECT Z.* FROM(SELECT X.*, ceil( rownum / %s ) as page FROM ( SELECT ID,SUBJECT,NAME, CREATED_DATE, MEMO,HITS FROM MAIN_NOTICEBOARD  ORDER BY ID DESC ) X ) Z WHERE page = %s', [rowsPerPage, current_page])

    print ('boardList=',boardList, 'count()=', totalCnt)

    # 전체 페이지를 구해서 전달...
    pagingHelperIns = pagingHelper();
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)

    print ('totalPageList', totalPageList)
    context = {
        'boardList':boardList,
        'totalCnt':totalCnt,
        'current_page':current_page,
        'totalPageList':totalPageList,
    }
    return render(request,'main/listSpecificPage.html',context)

def show_write_form(request):
    return render(request, 'main/writeBoard.html')

def viewWork(request):
    pk = request.GET['memo_id']
    boardData = NoticeBoard.objects.get(id=pk)


# 조회수를 늘린다.    
    NoticeBoard.objects.filter(id=pk).update(hits = boardData.hits + 1)


    return render(request,'main/viewMemo.html', {'memo_id': request.GET['memo_id'],
                                            'current_page':request.GET['current_page'],
                                            'searchStr': request.GET['searchStr'],
                                            'boardData': boardData } )


def listSpecificPageWork_to_update(request): # edit
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']
    boardData = NoticeBoard.objects.get(id=memo_id)
    return render(request,'main/viewForUpdate.html', {'memo_id': request.GET['memo_id'],
                                                'current_page':request.GET['current_page'],
                                                'searchStr': request.GET['searchStr'],
                                                'boardData': boardData } )    
@csrf_exempt
def updateBoard(request):
    memo_id = request.POST['memo_id']
    current_page = request.POST['current_page']

    # Update DataBase
    NoticeBoard.objects.filter(id=memo_id).update(
                                                  subject= request.POST['subject'],
                                                  memo= request.POST['memo']
                                                  )

    # Display Page => POST 요청은 redirection으로 처리하자
    url = '/listSpecificPageWork?current_page=' + str(current_page)
    return redirect(url)

def DeleteSpecificRow(request):
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']

    p = NoticeBoard.objects.get(id=memo_id)
    p.delete()
    
    # 마지막 메모를 삭제하는 경우, 페이지를 하나 줄임.
    totalCnt = NoticeBoard.objects.all().count()
    pagingHelperIns = pagingHelper();

    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
    print ('totalPages', totalPageList)

    if( int(current_page) in totalPageList):
        print ('current_page No Change')
        current_page=current_page
    else:
        current_page= int(current_page)-1
        print ('current_page--')

    url = '/listSpecificPageWork?current_page=' + str(current_page)
    return redirect(url)
#########################################################################################

# search
def searchWork(request):
    current_chk = request.GET['current_chk']

    user = request.user
    datas = chk_value.objects.filter(user=user).order_by('-pk')

    # 전 교과 성적 구하기.
    # 이수단위 반영 -> 이수단위 * 등급 / 이수단위 합
    isu = input_data.objects.filter(user=user)
    isu_sum = input_data.objects.filter(user=user).aggregate(Sum('complete_unit'))
    isu_mul_rate=0
    total_isu=0
    for s in isu:
        isu_mul_rate+=s.complete_unit*s.rate
    if(isu_sum['complete_unit__sum']):
        total_isu = round(isu_mul_rate/isu_sum['complete_unit__sum'],1)
    avgs = input_data.objects.filter(user=user).aggregate(Avg('rate'))

    # 주요 과목 평균 구하기.
    # 문/이과 확인
    if Profile.objects.get(user=user).type=="이과": # 이과인 경우
        p_isu = input_data.objects.filter(user=user).filter(~Q(subject1="예체능"),~Q(subject1="사회"))
    else:   #문과인경우
        p_isu = input_data.objects.filter(user=user).filter(~Q(subject1="예체능"),~Q(subject1="과학"))

    p_isu_sum = p_isu.aggregate(Sum('complete_unit'))
    p_isu_mul_rate=0
    data2=0
    for s in p_isu:
        p_isu_mul_rate+=s.complete_unit*s.rate
    if(p_isu_sum['complete_unit__sum']):
        data2 = round(p_isu_mul_rate/p_isu_sum['complete_unit__sum'],1)

    context = {
        'current_chk':current_chk,
        'chk_value':datas,
        'avg_rate':total_isu,
        #'avg_rate':avgs['rate__avg'],   # rate 평균 . dic 형태이기에 저런 식으로 써줘야 함. 
        'p_avg_rate':data2
    }

    return render(request,'main/searchWork.html',context)

# 선호지역 받기1
@csrf_exempt
def save_chk1(request):
    if 'preferRegions0' in request.POST:
        preferRegions0 = request.POST['preferRegions0']
    else:
        preferRegions0 = False
    chk = chk_value (user = request.user,
                     preferwhere1 = request.POST.get('preferRegions0'),
                     preferwhere2 = request.POST['preferRegions1'],
                     preferwhere3 = request.POST['preferRegions2'],
                     prefertype1 = request.POST['college0'],
                     prefertype2 = request.POST['college1'],
                     prefertype3 = request.POST['college2'],
                     prefertype4 = request.POST['college3'],
                     prefertype5 = request.POST['college4'],
                     prefertype6 = request.POST['college5'],
                     created_date = timezone.now(),
            )
    chk.save()

    url = '../searchWork/?current_chk=2'# + str(current_chk)
    
    return redirect(url)

# 내신성적받기2
@csrf_exempt
def save_chk(request):
    user = request.user

    if 'absent' in request.POST:
        absent = request.POST['absent']
    else:
        absent = False

    # 최신 레코드 가져오기(수정중인)
    cid = chk_value.objects.filter(user=user).last()

    awardcnt= int(request.POST['awardsCnt'])+int(request.POST['awardsCnt2'])+int(request.POST['awardsCnt3'])+int(request.POST['awardsCnt4'])+int(request.POST['awardsCnt5'])
    
    chk_value.objects.filter(user=user).filter(id=cid.id).update(
                    total_avgrate = request.POST['avgRate'],     #평균 내신
                    main_avgrate = request.POST['avgRate2'],      #주요 내신
                    executive_cnt = request.POST['executiveCnt'],
                    absent = absent,
                    award_cnt = awardcnt
                )
    
    url = '../searchWork/?current_chk=3'# + str(current_chk)
    
    return redirect(url)

#동아리활동3
@csrf_exempt
def save_chk2(request):
    user = request.user
    circle_cnt= int(request.POST['circlesCnt'])+int(request.POST['circlesCnt2'])+int(request.POST['circlesCnt3'])+int(request.POST['circlesCnt4'])+int(request.POST['circlesCnt5'])+int(request.POST['circlesCnt6'])+int(request.POST['circlesCnt7'])+int(request.POST['circlesCnt8'])
    vol_cnt=int(request.POST['volunteerTime'])+int(request.POST['volunteerTime2'])
    reading_cnt=int(request.POST['readingCnt'])+int(request.POST['readingCnt2'])+int(request.POST['readingCnt3'])+int(request.POST['readingCnt4'])+int(request.POST['readingCnt5'])+int(request.POST['readingCnt6'])+int(request.POST['readingCnt7'])
   
    # Update DataBase
    # 최신 레코드 가져오기(수정중인)
    cid = chk_value.objects.filter(user=user).last()
    chk_value.objects.filter(user=user).filter(id=cid.id).update(
                                                circle_cnt= circle_cnt,
                                                volunteer= vol_cnt,
                                                reading=reading_cnt
                                            )

    url = '../searchWork/?current_chk=4'# + str(current_chk)
    return redirect(url)

def del_result(request):
    rid = request.GET.get('id',False)
    user=request.user
    p = chk_value.objects.get(id=rid)
    p.delete()
    url = '/result'
    return redirect(url)

# show_result/?id= []  값 얻어와서 넘겨줌.
# chk_value 에 해당 id 값의 데이터 가져오고, 그 chk_val에 해당하는 레코드를 search_history에서 가져옴.
def show_result(request):
    rid = request.GET['id']
    user=request.user
    p = chk_value.objects.get(id=rid)
    data_1 = search_history.objects.filter(ch_val=p).filter(r_type="소신")  # error?
    data_2 = search_history.objects.filter(ch_val=p).filter(r_type="적정")  # error?
    data_3 = search_history.objects.filter(ch_val=p).filter(r_type="안정") # error?

    context = {
        's1_history':data_1,
        's2_history':data_2,
        's3_history':data_3,
    }
    return render(request,'main/show_prev.html',context)


# 404 error page handle
def handler404(request, *args, **argv):
    response = render(request, "main/404.html", {})
    response.status_code = 404
    return response

 

def handler500(request, *args, **argv):
    response = render(request, "main/500.html", {})
    response.status_code = 500
    return response

@csrf_exempt
def idcheck(request):
    username = request.POST.get('h_username')
    if User.objects.filter(username=username).exists():
        messages.error(request,'중복된 아이디입니다!')
    else:
        messages.success(request, '등록 가능한 아이디입니다.')
    context={
        'id': username,
    }
    return render(request,'main/signup.html',context)