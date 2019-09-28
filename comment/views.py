from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

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

        parent = comment_form.cleaned_data['parent']
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        data = {
            'username':comment.user.username,
            # 格式化为当地时间
            'comment_time':timezone.localtime(comment.comment_time).strftime('%Y-%m-%d %H:%M:%S'),
            'comment_text':comment.text,
            'content_type': ContentType.objects.get_for_model(comment).model,
            'status':'SUCCESS',
            'pk':comment.pk,
            'root_pk':comment.root.pk if comment.root else '',
        }

        if parent:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0]
        }

    return JsonResponse(data)



