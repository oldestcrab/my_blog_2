from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import  User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING, verbose_name='用户')

    # 顶级评论
    root = models.ForeignKey('self', related_name='root_comment', on_delete=models.DO_NOTHING, null=True, verbose_name='顶级评论')
    # 评论指向谁
    parent = models.ForeignKey('self', related_name='parent_comment', on_delete=models.DO_NOTHING, null=True, verbose_name='父辈评论')
    # 回复谁的评论
    reply_to = models.ForeignKey(User, related_name='replies', on_delete=models.DO_NOTHING, null=True, verbose_name='指向评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-comment_time']
