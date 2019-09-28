from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

def SuccessResponse(liked_num):
    data = {
        'status': 'SUCCESS',
        'liked_num': liked_num,
    }
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {
        'status': 'ERROR',
        'code': code,
        'message': message,
    }
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '尚未登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '点赞对象不存在')

    # 判断是点赞还是取消点赞
    if request.GET.get('is_like') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            return ErrorResponse(402, '您已赞过')

    else:
        # 判断是否已点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数-1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.like_num)
            else:
                return ErrorResponse(404, '数据错误')
        else:
            return ErrorResponse(403, '没有点赞过')