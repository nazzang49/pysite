from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook

# 방명록 리스트
def list(request):
    # 가장 최신 방명록부터 추출
    guestbooklist = Guestbook.objects.all().order_by('-id')
    data = {
        'guestbooklist': guestbooklist
    }
    return render(request, 'guestbook/list.html', data)

# 방명록 추가
def add(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.content = request.POST['content']

    guestbook.save()
    # redirect
    return HttpResponseRedirect('/guestbook/')

def deleteform(request, id=0):
    data = {
        'id': id
    }
    return render(request, 'guestbook/deleteform.html', data)

def delete(request):
    guestbook = Guestbook.objects.filter(id=request.POST['id']).filter(password=request.POST['password'])
    guestbook.delete()
    return HttpResponseRedirect('/guestbook/')