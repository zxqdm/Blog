from django.urls import path
from blog import views

urlpatterns = [
    path('blog/', views.all_blog),
    path('tags/', views.tags),
    path('article/', views.blog),
    path('articleAdd/', views.article_add),
    path('saveImg/', views.save_img),
    path('comment/', views.show_comment),
    path('commentAdd/', views.comment_add),
    path('replyAdd/', views.reply_add),
]
