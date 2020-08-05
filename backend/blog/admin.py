from django.contrib import admin
from blog.models import Blog, Tag, Comment, Reply
# Register your models here.


admin.site.register([Blog, Tag, Comment, Reply])
