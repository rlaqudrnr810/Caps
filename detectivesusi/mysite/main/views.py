from django.shortcuts import render, redirect

from .forms import LoginForm
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from .forms import LoginForm, SignupForm

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

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

###########################################

