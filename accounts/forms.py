from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    """用户登录表单

    """
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        """判断数据是否有效

        :return:
        """
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            self.cleaned_data['user'] = user
        else:
            raise ValidationError('用户名或者密码错误')

        return self.cleaned_data

class RegisterForm(forms.Form):
    """用户注册表单

    """
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='密码确认', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入密码'}))

    def clean_username(self):
        """判断用户名是否有效

        :return:
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        """判断邮箱是否有效

        :return:
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        """判断密码是否一致

        :return:
        """
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise ValidationError('两次密码不一致')
        return password_again
