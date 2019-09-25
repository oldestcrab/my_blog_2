from django.contrib import admin
from .models import BlogType, Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_read_num', 'blog_type', 'created_time', 'last_update_time', 'is_delete')

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')