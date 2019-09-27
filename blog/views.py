from django.shortcuts import render
from .models import Blog, BlogType
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from read_statistics.utils import read_statistics_once_read
from comment.forms import CommentForm
from comment.models import Comment

def get_blog_list_common_date(request, object_list):
    """返回博客的一些通用信息

    :param request: request
    :param object_list: object列表
    :return: context
    """
    # 获取页码，没有则默认1
    page = request.GET.get('page', 1)

    # 获取分页器，每页7篇博客
    paginator = Paginator(object_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # 当前页对象
    current_page = paginator.get_page(page)
    # 当前页码数
    current_page_num = current_page.number
    # 获取页码列表，前二后二
    page_range = list(range(max(current_page_num-2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num+3, paginator.num_pages+1)))

    # 如果当前页大于第3页，显示第一页
    if current_page_num-2 >1:
        page_range.insert(0, '...')
        page_range.insert(0, 1)

    # 如果当前页小于倒数第3页，显示最后一页
    if current_page_num+2<paginator.num_pages:
        page_range.append('...')
        page_range.append(paginator.num_pages)

    # 按月分类, 以及数量统计
    blog_dates_dict = {}
    for blog in Blog.objects.dates('created_time', 'month', 'DESC'):
        blog_count = Blog.objects.filter(created_time__year=blog.year, created_time__month=blog.month).count()
        blog_dates_dict[blog] = blog_count

    # 所有博客分类, 以及数量统计
    blog_types_count = BlogType.objects.annotate(blog_count=Count('blog'))

    context = {
        'blog_types': blog_types_count,
        'page_range': page_range,
        'current_page': current_page,
        'blog_dates_dict': blog_dates_dict,
    }

    return context

def blog_list(request):
    """展示所有博客列表

    :param request: request
    :return:
    """
    # 获取所有博客
    blogs = Blog.objects.all()
    context = get_blog_list_common_date(request, blogs)
    return render(request, 'blog/blog_list.html', context=context)

def blogs_with_type(request, blog_with_type_id):
    """展示通过博客标签分类的博客列表

    :param request: request
    :param blog_with_type_id: 博客标签ID
    :return:
    """
    # 当前博客分类
    blog_type = get_object_or_404(BlogType, id=blog_with_type_id)
    # 当前博客分类的所有博客
    blogs_with_type = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_date(request, blogs_with_type)

    context['blog_type'] = blog_type

    return render(request, 'blog/blog_with_type.html', context=context)

def blogs_with_date(request, year, month):
    """展示通过日期(月份)分类的博客列表

    :param request: request
    :param year: 年份
    :param month: 月份
    :return:
    """

    # 当前日期的所有博客
    blogs_with_date = Blog.objects.filter(created_time__year=year, created_time__month=month)

    context = get_blog_list_common_date(request, blogs_with_date)

    context['blogs_with_date'] = blogs_with_date
    context['current_date'] = str(year) + '-' + str(month)
    return render(request, 'blog/blog_with_type.html', context=context)

def blog_detail(request, blog_id):
    """展示博客详细信息

    :param request: request
    :param blog_id: 博客ID
    :return:
    """
    # 通过id获取博客对象
    blog = get_object_or_404(Blog, id=blog_id)

    # 返回设置的cookies key
    key = read_statistics_once_read(request, blog)

    # 上一条博客
    previous_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()

    # 下一条博客
    next_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()

    content_type = ContentType.objects.get_for_model(blog)
    # 获取评论列表
    comments = Comment.objects.filter(content_type=content_type, object_id=blog.pk, parent=None)

    context = {
        'blog': blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        'comments': comments,
        # 评论表单实例化
        'comment_form': CommentForm(initial={'object_id':blog.pk, 'content_type': content_type.model, 'reply_comment_id':0})
    }

    response = render(request, 'blog/blog_detail.html', context=context)
    response.set_cookie(key, 'true')

    return response