from django.db import models
from user.models import User


# 博客表
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_show = models.IntegerField(default=0)
    visit_num = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE)


# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=100)
    blog = models.ManyToManyField(to=Blog, related_name='tags')


# 评论表
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    from_uid = models.ManyToManyField(to=User)
    bid = models.ForeignKey(to=Blog, to_field='id', on_delete=models.CASCADE)


class Reply(models.Model):
    content = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    comment_id = models.ForeignKey(to=Comment, to_field='id', on_delete=models.CASCADE)
    from_uid = models.ManyToManyField(to=User)
    to_uid = models.IntegerField(null=True)
    reply_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


