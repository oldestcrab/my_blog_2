from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment

def update_comment(request):
    """返回通过ajax提交的评论

    :param request: request
    :return: json数据
    """
    comment_form = CommentForm(request.POST, user=request.user)
    # 数据没问题则保存
    if comment_form.is_valid():
        comment = Comment()
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.text = comment_form.cleaned_data['text']
        comment.user = request.user
        comment.save()

        data = {
            'username':comment.user.username,
            'comment_time':comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'comment_text':comment.text,
            'status':'SUCCESS',
        }

    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0]
        }

    return JsonResponse(data)



