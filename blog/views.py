from django.shortcuts import render
from .models import Blog, BlogType
from django.shortcuts import get_object_or_404


def blog_list(request):
    blogs = Blog.objects.all()

    context = {
        'blogs': blogs,
    }

    return render(request, 'blog/blog_list.html', context=context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    context = {
        'blog': blog,
    }

    return render(request, 'blog/blog_detail.html', context=context)

def blog_with_type(request, blog_with_type_id):
    blog_type = get_object_or_404(BlogType, id=blog_with_type_id)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = {
        'blogs': blogs,
    }

    return render(request, 'blog/blog_with_type.html', context=context)