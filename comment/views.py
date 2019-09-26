from django.shortcuts import render
from .forms import CommentForm

def update_comment(request):
    comment_form = CommentForm


