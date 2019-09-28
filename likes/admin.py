from django.contrib import admin
from .models import LikeCount, LikeRecord

@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'like_num', 'content_type', 'object_id',)

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'liked_time', 'content_type', 'object_id',)