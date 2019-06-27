from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User

# 회원가입 페이지 이동
def joinform(request):
    return render(request,'user/joinform.html')

# 가입 성공 시 페이지 이동
def joinsuccess(request):
    return render(request,'user/joinsuccess.html')

# 회원가입
def join(request):
    user = User()
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    # joindate는 자동(now)으로 입력됨

    user.save()
    # redirect
    return HttpResponseRedirect('/user/joinsuccess')

# 로그인 페이지 이동
def loginform(request):
    return render(request,'_bs/user/loginform.html')

# 로그인 + 세션 처리
def login(request):
    # user 테이블에서 해당 조건 만족하는 튜플 추출(list 타입 반환)
    results = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])

    # 로그인 실패
    if len(results)==0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 성공 + 세션 처리
    authuser = results[0]
    # 세션은 dict 타입으로 저장되므로, dict로 타입 캐스팅 해준다
    request.session['authuser'] = model_to_dict(authuser)

    return HttpResponseRedirect('/')

def logout(request):
    # 세션 삭제
    del request.session['authuser']
    return HttpResponseRedirect('/')

def updateform(request):
    # 기존 회원 정보
    user = User.objects.get(id=request.session['authuser']['id'])
    data = {
        'user':user
    }
    return render(request, 'user/updateform.html', data)

def update(request):
    # request.session['authuser']['id'] >> authuser dict 내 dict 중 id
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']
    user.gender = request.POST['gender']
    # 비밀번호가 없으면
    if request.POST['password'] is not '':
        user.password = request.POST['password']

    user.save()

    # 변경된 정보 세션 반영
    request.session['authuser']['name'] = user.name
    return HttpResponseRedirect('/user/updateform?result=success')

def checkemail(request):
    email = request.GET['email']
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        user = None
    result = {
        'result':'success',
        'data':'not exist' if user is None else 'exist'
    }
    return JsonResponse(result)












