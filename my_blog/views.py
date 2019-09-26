#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: views.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/24 15:23
# @description： 主页视图

import datetime
from django.shortcuts import render, redirect
from read_statistics.utils import get_seven_days_read_data, get_range_day_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib import auth


def home(request):

    content_type = ContentType.objects.get_for_model(Blog)
    # 前七天的日期，以及博客阅读数量列表
    days, read_nums = get_seven_days_read_data(content_type)

    # 今天热门博客
    range_day_hot_blogs_0 = get_range_day_hot_blogs(0)
    # 昨天热门博客
    range_day_hot_blogs_1 = get_range_day_hot_blogs(1)

    # 使用缓存，过去一周热门博客
    range_day_hot_blogs_7 = cache.get('range_day_hot_blogs_7')
    if not range_day_hot_blogs_7:
        range_day_hot_blogs_7 = get_range_day_hot_blogs(7)
        cache.set('range_day_hot_blogs_7', range_day_hot_blogs_7, 3600)

    # 使用缓存，过去一个月热门博客
    range_day_hot_blogs_30 = cache.get('range_day_hot_blogs_30')
    if not range_day_hot_blogs_30:
        range_day_hot_blogs_30 = get_range_day_hot_blogs(30)
        cache.set('range_day_hot_blogs_30', range_day_hot_blogs_30, 3600)

    context = {
        'read_nums': read_nums,
        'days': days,
        'range_day_hot_blogs_0': range_day_hot_blogs_0,
        'range_day_hot_blogs_1': range_day_hot_blogs_1,
        'range_day_hot_blogs_7': range_day_hot_blogs_7,
        'range_day_hot_blogs_30': range_day_hot_blogs_30,
    }
    return render(request, 'home.html', context=context)

def login(request):
    username = request.POST.get('user')
    password = request.POST.get('password')

    user = auth.authenticate(request=request, username=username, password=password)
    if user:
        auth.login(request, user)
        return redirect('/')
    else:
        pass