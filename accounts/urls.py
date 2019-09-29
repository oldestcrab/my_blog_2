from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login_for_modal', views.login_for_modal, name='login_for_modal'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('user_info', views.user_info, name='user_info'),
    path('change_nickname', views.change_nickname, name='change_nickname'),
    path('bind_email', views.bind_email, name='bind_email'),
    path('send_verification_code', views.send_verification_code, name='send_verification_code'),
]

