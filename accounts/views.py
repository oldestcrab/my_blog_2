#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: views.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/24 15:23
# @description： 主页视图

from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm

def register(request):
    """用户注册视图

    :param request: request
    :return:
    """
    if request.method == 'POST':
        # 表单验证
        reg_form = RegisterForm(request.POST)
        # 判断数据是否有效，有则创建用户
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            # 注册成功，跳转到登录页面
            return redirect('accounts:login')
    else:
        # 实例化注册表单
        reg_form = RegisterForm()

    context = {
        'reg_form': reg_form,
    }
    return render(request, 'accounts/register.html', context=context)

def login_for_modal(request):
    """用户通过弹出窗口登录视图

    :param request:
    :return: 登录状态，SUCCESS or ERROR
    """
    # 表单验证
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        # 登录
        auth.login(request, user)

        data = {
            'status': 'SUCCESS',
        }
    else:
        data = {
            'status': 'ERROR',
        }

    return JsonResponse(data)

def login(request):
    """用户登录视图

    :param request: request
    :return:
    """
    # 如果提交方式为post,传输数据给登录表单，否则返回空表单
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 判断数据是否有效，有则登录，跳转到之前的页面或者首页
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            # 登录
            auth.login(request, user)
            # 跳转回之前的页面
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 实例化登录表单
        login_form = LoginForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'accounts/login.html', context=context)

def logout(request):
    """退出登录视图

    :param request:
    :return:
    """
    auth.logout(request)
    # 跳转到之前的页面
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    """用户中心视图

    :param request:
    :return:
    """
    context = {

    }

    return render(request, 'accounts/user_info.html', context=context)