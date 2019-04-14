from django.contrib.auth.models import User
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

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def search_result(request):
    return render(request, 'main/search_result.html')    

def mypage(request):
    return render(request, 'main/mypage.html')

def result(request):
    return render(request, 'main/result.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
	return render(request, 'main/contact.html')

def search(request):
	return render(request, 'main/search.html')

def faq(request):
	return render(request, 'main/faq.html')

## login & sign up ##
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
            signup_form.signup()
            return redirect('main:home')
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

#search
def searchWork(request):
    current_chk = request.GET['current_chk']

    # search 에서 선택한 값들 db에 저장.
    # username = None
    # if request.user.is_authenticated:
    #     username = request.user.username

    # print ('current_chk=', current_chk)

    #preferwhere_answer = request.GET['preferRegions[]'] 
    #                 # preferwhere1=request.POST['preferRegions[]'],
    #                 # preferwhere2=request.POST['memo'],
    #                 # preferwhere3=request.POST['memo'],
    #                 # prefertype1=request.POST['memo'],
    #                 # prefertype2=request.POST['memo'],
    #                 # prefertype3=request.POST['memo'],
    #                 # prefertype4=request.POST['memo'],
    #                 # prefertype5=request.POST['memo'],
    #                 # prefertype6=request.POST['memo'],
    #                 # prefertype7=request.POST['memo'],
    #                  )

    user = request.user
    datas = chk_value.objects.filter(user=user)
    context = {
        'current_chk':current_chk,
        'chk_value':datas
    }
    return render(request,'main/searchWork.html',context)

# 회원 가입시 테이블 하나를 미리 생성 해둔 뒤 update 방식으로 해야할듯.(중복 테이블 계속 생김.)
# 중복된 테이블 있는지 보는것도 괜찮을듯.

# 내신성적받기
@csrf_exempt
def save_chk(request):
    user = request.user
    # current_chk = request.GET['current_chk']
    # user = User.objects.get(id=username)
    # username = None
    # if request.user.is_authenticated:
    #     username = request.user.username

    if 'absent' in request.POST:
        absent = request.POST['absent']
    else:
        absent = False
    
    awardcnt= int(request.POST['awardsCnt'])+int(request.POST['awardsCnt2'])+int(request.POST['awardsCnt3'])+int(request.POST['awardsCnt4'])+int(request.POST['awardsCnt5'])
    chk_value.objects.filter(user=user).update(
                    total_avgrate = request.POST['avgRate'],     #평균 내신
                    main_avgrate = request.POST['avgRate2'],      #주요 내신
                    executive_cnt = request.POST['executiveCnt'],
                    absent = absent,
                    award_cnt = awardcnt
                )
    
    url = '../searchWork/?current_chk=3'# + str(current_chk)
    
    return redirect(url)

# 선호지역 받기
@csrf_exempt
def save_chk1(request):
    if 'preferRegions0' in request.POST:
        preferRegions0 = request.POST['preferRegions0']
    else:
        preferRegions0 = False
    chk = chk_value (user = request.user,
                     preferwhere1 = request.POST['preferRegions0'],
                     preferwhere2 = request.POST['preferRegions1'],
                     preferwhere3 = request.POST['preferRegions2'],
                     prefertype1 = request.POST['college0'],
                     prefertype2 = request.POST['college1'],
                     prefertype3 = request.POST['college2'],
                     prefertype4 = request.POST['college3'],
                     prefertype5 = request.POST['college4'],
                     prefertype6 = request.POST['college5'],
            )
    chk.save()
    
    url = '../searchWork/?current_chk=2'# + str(current_chk)
    
    return redirect(url)

#동아리활동
@csrf_exempt
def save_chk2(request):
    user = request.user
    circle_cnt= int(request.POST['circlesCnt'])+int(request.POST['circlesCnt2'])+int(request.POST['circlesCnt3'])+int(request.POST['circlesCnt4'])+int(request.POST['circlesCnt5'])+int(request.POST['circlesCnt6'])+int(request.POST['circlesCnt7'])+int(request.POST['circlesCnt8'])
    vol_cnt=int(request.POST['volunteerTime'])+int(request.POST['volunteerTime2'])
    reading_cnt=int(request.POST['readingCnt'])+int(request.POST['readingCnt2'])+int(request.POST['readingCnt3'])+int(request.POST['readingCnt4'])+int(request.POST['readingCnt5'])+int(request.POST['readingCnt6'])+int(request.POST['readingCnt7'])
    # Update DataBase
    chk_value.objects.filter(user=user).update(
                                                circle_cnt= circle_cnt,
                                                volunteer= vol_cnt,
                                                reading=reading_cnt
                                            )

    url = '../searchWork/?current_chk=4'# + str(current_chk)
    return redirect(url)

# def search_final(request):
#     user = request.user
#     datas = chk_value.objects.filter(user=user)

#     return render(request, '', {'chk_value':datas})