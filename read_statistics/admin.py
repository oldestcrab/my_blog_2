from django.contrib import admin
from .models import ReadNum, ReadNumDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'read_num', 'content_type', 'object_id', 'content_object')

@admin.register(ReadNumDetail)
class ReadNumDetailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'read_num', 'date', 'content_type', 'object_id', 'content_object')