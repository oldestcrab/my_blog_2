from ..models import Comment
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    """获取具体的某个模型对象的评论数

    :param obj: 具体的某个模型对象
    :return: 具体的某个模型对象的评论数
    """
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()

@register.simple_tag
def get_comment_form(obj):
    """获取评论初始表单

    :param obj: 具体的某个模型对象
    :return: 评论初始表单
    """
    content_type = ContentType.objects.get_for_model(obj).model
    form = CommentForm(initial={
        'content_type': content_type,
        'object_id': obj.id,
        'reply_comment_id': 0,
    })
    return form

@register.simple_tag
def get_comments_list(obj):
    """获取评论列表

    :param obj: 具体的某个模型对象
    :return: 评论列表
    """
    content_type = ContentType.objects.get_for_model(obj)
    # 获取评论列表
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')