from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request,'user/joinform.html')

def joinsuccess(request):
    return render(request,'user/joinsuccess.html')

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

def loginform(request):
    return render(request,'user/loginform.html')