#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: views.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/24 15:23
# @description： 主页视图

from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_date
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

def home(request):

    content_type = ContentType.objects.get_for_model(Blog)
    # 前七天的日期，以及博客阅读数量列表
    days, read_nums = get_seven_days_read_date(content_type)
    context = {
        'read_nums': read_nums,
        'days': days,
    }
    return render(request, 'home.html', context=context)
