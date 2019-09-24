from django.shortcuts import render
from .models import Blog, BlogType
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.conf import settings


def get_blog_common_date(request, object_list):
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

    # 所有博客分类
    blog_types = BlogType.objects.all()

    context = {
        'blog_types': blog_types,
        'page_range': page_range,
        'current_page': current_page,
    }

    return context

def blog_list(request):
    """展示所有博客列表

    :param request: request
    :return:
    """
    # 获取所有博客
    blogs = Blog.objects.all()
    context = get_blog_common_date(request, blogs)
    return render(request, 'blog/blog_list.html', context=context)

def blog_with_type(request, blog_with_type_id):
    """展示通过博客标签分类的博客列表

    :param request: request
    :param blog_with_type_id: 博客标签ID
    :return:
    """
    # 当前博客分类
    blog_type = get_object_or_404(BlogType, id=blog_with_type_id)
    # 当前博客分类的所有博客
    blogs_with_type = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_common_date(request, blogs_with_type)

    # 所有博客分类
    blog_types = BlogType.objects.all()

    context['blog_types'] = blog_types
    context['blog_type'] = blog_type

    return render(request, 'blog/blog_with_type.html', context=context)

def blog_detail(request, blog_id):
    """展示博客详细信息

    :param request: request
    :param blog_id: 博客ID
    :return:
    """
    # 通过id获取博客对象
    blog = get_object_or_404(Blog, id=blog_id)

    context = {
        'blog': blog,
    }

    return render(request, 'blog/blog_detail.html', context=context)