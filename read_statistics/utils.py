import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadNumDetail
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog


def read_statistics_once_read(request, obj):
    """判断是否需要+1或者创建模型阅读数

    :param request: request
    :param obj: 模型对象
    :return: cookies key,表示已阅读
    """
    content_type = ContentType.objects.get_for_model(obj)
    # 设置cookies key
    key = f'{content_type.model}_{obj.pk}_read'
    # 如果cookies没有相关信息，则阅读数+1
    if not request.COOKIES.get(key):
        # 博客阅读数量模型，+1或者创建博客阅读数
        readnum, create = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当前时间
        date = timezone.now().date()
        # 博客详细阅读数量模型，+1或者创建当天的博客阅读数
        readNumDetail, create = ReadNumDetail.objects.get_or_create(content_type=content_type, object_id=obj.pk, date=date)
        readNumDetail.read_num += 1
        readNumDetail.save()

    return key

def get_seven_days_read_data(content_type):
    """获取前七天的相关模型阅读数量

    :param content_type: content_type
    :return: 前七天的日期，以及前七天的相关模型阅读数量列表
    """
    # 获取今天日期
    today = timezone.now().date()
    days = []
    read_nums = []

    # 遍历前7天
    for i in range(7, 0, -1):
        day = today - datetime.timedelta(days=i)
        days.append(day.strftime('%m/%d'))
        result_detail = ReadNumDetail.objects.filter(content_type=content_type, date=day)
        # 获取某天的总博客阅读数量
        result_blog = result_detail.aggregate(read_count=Sum('read_num'))
        read_nums.append(result_blog['read_count'] or 0)

    return days, read_nums

def get_oneday_hot_blogs(content_type, date):
    """获取某一天的前7篇博客以及当天浏览量

    :param content_type: content_type
    :param date: 某一天的日期
    :return: 某一天的前7篇博客以及当天浏览量
    """
    # 获取阅读量排行前7的博客
    today_hot_blogs = ReadNumDetail.objects.filter(content_type=content_type, date=date).order_by('-read_num')[:7]
    # print(today_hot_blogs)
    return today_hot_blogs

def get_range_day_hot_blogs(days:int):
    """获取前某天范围内的热门博客

    :param days: 前几天范围内的热门阅读，前7天：7，当天：0
    :return: 前某天范围内的热门博客字典
    """
    # 前某天的日期
    date =  timezone.now().date() - datetime.timedelta(days)

    # 热门博客字典
    hot_blogs_data = Blog.objects.filter(read_num_details__date__gte=date) \
                    .values('id', 'title').annotate(read_num_detail=Sum('read_num_details__read_num')).order_by('-read_num_detail')[:7]

    return hot_blogs_data