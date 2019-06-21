from django.db import models

# Create your models here.
from user.models import User

class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    hit = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    # 유저 객체를 포린키로 설정 (ORM 설계의 기본 방식)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)