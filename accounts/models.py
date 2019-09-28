from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """关联自带的用户模型

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name='昵称')

    def __str__(self):
        return f'<Profile:{self.nickname} for {self.user}>'

def get_nickname(self):
    """获取昵称

    :param self:
    :return: 昵称或者空字符串
    """
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

def get_nickname_or_username(self):
    """获取昵称或者用户名

    :param self:
    :return: 昵称或者用户名
    """
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


def has_nickname(self):
    """判断是否有昵称

    :param self:
    :return: True or False
    """
    return Profile.objects.filter(user=self).exists()

# 动态绑定
User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
