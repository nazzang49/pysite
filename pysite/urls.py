"""pysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

# 모듈 생성
import board.views
import guestbook.views
import main.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.index),

    # 회원
    path('user/joinform', user.views.joinform),
    path('user/joinsuccess', user.views.joinsuccess),
    path('user/join', user.views.join),
    path('user/loginform', user.views.loginform),
    path('user/login', user.views.login),
    path('user/logout', user.views.logout),
    path('user/updateform', user.views.updateform),
    path('user/update', user.views.update),
    path('user/api/checkemail', user.views.checkemail),

    # 방명록
    path('guestbook/', guestbook.views.list),
    path('guestbook/add', guestbook.views.add),
    path('guestbook/deleteform/<int:id>', guestbook.views.deleteform),
    path('guestbook/delete', guestbook.views.delete),

    # 게시판
    path('board/', board.views.list),
    path('board/write', board.views.write),
    path('board/write_one', board.views.write_one),
    path('board/view', board.views.view),
    path('board/modify', board.views.modify),
    path('board/modify_one', board.views.modify_one),
    path('board/rewrite', board.views.rewrite),
    path('board/rewrite_one', board.views.rewrite_one),
    path('board/delete', board.views.delete),
    # re_path test(get, post 동시 처리)
    re_path(r'^board/comment(?:/(?P<commentid>\d+))?/$', board.views.comment)
]
