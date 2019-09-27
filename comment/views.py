from django.shortcuts import render, reverse, redirect
from .forms import CommentForm
from .models import Comment

def update_comment(request):
    # 获取跳转之前的url
    refer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    # 数据没问题则保存
    if comment_form.is_valid():
        comment = Comment()
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.text = comment_form.cleaned_data['text']
        comment.user = request.user
        comment.save()

    return redirect(refer)


