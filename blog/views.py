from django.shortcuts import render
from .models import Blog, BlogType
from django.shortcuts import get_object_or_404


def blog_list(request):
    # 所有博客
    blogs = Blog.objects.all()
    # 所有博客分类
    blog_types = BlogType.objects.all()

    context = {
        'blogs': blogs,
        'blog_types': blog_types,
    }

    return render(request, 'blog/blog_list.html', context=context)


def blog_detail(request, blog_id):
    # 通过id获取博客对象
    blog = get_object_or_404(Blog, id=blog_id)

    context = {
        'blog': blog,
    }

    return render(request, 'blog/blog_detail.html', context=context)

def blog_with_type(request, blog_with_type_id):
    # 当前博客分类
    blog_type = get_object_or_404(BlogType, id=blog_with_type_id)
    # 当前博客分类的所有博客
    blogs = Blog.objects.filter(blog_type=blog_type)
    # 所有博客分类
    blog_types = BlogType.objects.all()

    context = {
        'blogs': blogs,
        'blog_type': blog_type,
        'blog_types': blog_types,
    }

    return render(request, 'blog/blog_with_type.html', context=context)