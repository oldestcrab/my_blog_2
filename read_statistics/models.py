from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class ReadNum(models.Model):
    # 相关模型阅读总数量
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod():

    def get_read_num(self):
        """获取博客等的阅读数

        :return: 阅读数，无则返回0
        """
        try:
            content_type = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=content_type, object_id=self.pk)
            return readnum.read_num
        except ObjectDoesNotExist:
            return 0

class ReadNumDetail(models.Model):
    # 相关模型某日阅读总数量
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')