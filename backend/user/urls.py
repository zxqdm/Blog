from django.urls import path
from user import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('profile/', views.profile),
    path('profile/change/', views.profile_change),
]