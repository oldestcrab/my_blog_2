from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'comment_time', 'text', 'content_type', 'object_id', 'parent', 'root', 'reply_to',)