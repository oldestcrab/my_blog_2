from django import forms
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    text = forms.CharField(label=False, widget=CKEditorWidget(config_name='comment_ckeditor'))
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id',}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            # 判断是否存在模型对象
            model_class = ContentType.objects.get(model=content_type).model_class()
            # 模型对象获取数据
            model_obj = model_class.objects.get(pk=object_id)

            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise ValidationError('评论对象不存在')

        # 判断用户是否存在
        if not self.user.is_authenticated:
            raise ValidationError('用户信息不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id<0:
            raise ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise ValidationError('回复出错')

        return reply_comment_id