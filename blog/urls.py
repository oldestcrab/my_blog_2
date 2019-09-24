from django.urls import path
from django.conf import urls
from blog import views
app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_with_type_id>', views.blog_with_type, name='blog_with_type'),
]
