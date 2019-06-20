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
from django.urls import path

# 모듈 생성
import guestbook.views
import main.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.index),
    path('user/joinform', user.views.joinform),
    path('user/joinsuccess', user.views.joinsuccess),
    path('user/join', user.views.join),
    path('guestbook/', guestbook.views.list),
    path('guestbook/add', guestbook.views.add),
    path('guestbook/deleteform/<int:id>', guestbook.views.deleteform),
    path('guestbook/delete', guestbook.views.delete),
]
