from django.db import models


# 用户表
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16)
    email = models.EmailField()
    password = models.CharField(max_length=16)
    access = models.IntegerField(default=0)
    avatar = models.CharField(max_length=1000, default="defaultAvatar.jpg")
    created = models.DateTimeField(auto_now_add=True)
