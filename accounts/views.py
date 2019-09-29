#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: views.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/24 15:23
# @description： 主页视图

import random
import string
import time

from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm, ChangeNicknameForm, BindEmailForm
from .models import Profile

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

def change_nickname(request):
    """修改昵称视图

    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递数据给昵称修改表单
        form = ChangeNicknameForm(request.POST, user=request.user)
        # 数据验证
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            # 修改保存
            profile.nickname = nickname_new
            profile.save()
            # 跳转回之前的页面
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 实例化昵称表单
        context = {
            'page_title': '修改昵称',
            'form_title': '修改昵称',
            'submit_text': '修改',
            'return_back_url': request.GET.get('from', reverse('home')),
            'form': ChangeNicknameForm(),
        }
        return render(request, 'form.html', context=context)

def bind_email(request):
    """修改昵称视图

    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递数据给昵称修改表单
        form = BindEmailForm(request.POST, request=request)
        # 数据验证
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 跳转回之前的页面
            return redirect(request.GET.get('from', reverse('home')))

    else:
        # 实例化昵称表单
        form = BindEmailForm()
    context = {
        'page_title': '绑定邮箱',
        'form_title': '绑定邮箱',
        'submit_text': '绑定',
        'return_back_url': request.GET.get('from', reverse('home')),
        'form': form,
    }
    return render(request, 'accounts/bind_email.html', context=context)

def send_verification_code(request):
    email = request.get('email', '')
    data = {}
    if email:
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time <30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_mail(
                '绑定邮箱',
                f'验证码:{code}',
                '18819425701',
                [email],
                fail_silently=False,
            )

            data['status'] = 'SUCCESS'

    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)