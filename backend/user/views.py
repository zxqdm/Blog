import os
import uuid
import base64
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user import models
from myblog.settings import MEDIA_ROOT
from myblog.utils import mkdir

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_obj = models.User.objects.filter(username=username)[0]
        if user_obj:
            password = request.POST.get('password')
            if user_obj.password == password:
                access = user_obj.access
                avatar = user_obj.avatar
                starttime = time.time()
                endtime = starttime + 14 * 24 * 3600
                return JsonResponse({'status': 1,
                                     'message': '登录成功',
                                     'data': {
                                         'username': username,
                                         'access': access,
                                         'avatar': avatar,
                                         'starttime': str(starttime).split('.')[0],
                                         'endtime': str(endtime).split('.')[0],
                                     }})
            else:
                return JsonResponse({'status': 0,
                                     'message': '密码错误'})
        else:
            return JsonResponse({'status': 0,
                                 'message': '用户名不存在'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if models.User.objects.filter(username=username):
            return JsonResponse({'status': 0,
                                 'message': '用户名已存在'})
        else:
            password = request.POST.get('password')
            email = request.POST.get('email')
            models.User.objects.create(username=username,
                                       password=password,
                                       email=email)
            mkdir(MEDIA_ROOT, username)
            return JsonResponse({'status': 1,
                                 'message': '注册成功'})

@csrf_exempt
def profile(request):
    username = request.POST.get('username')
    user_obj = models.User.objects.filter(username=username)
    if user_obj:
        user_obj = user_obj[0]
        email = user_obj.email
        created = user_obj.created.strftime('%Y-%m-%d')
        return JsonResponse({'status': 1,
                             'data': {
                                 'username': username,
                                 'email': email,
                                 'created': created,
                             }})
    else:
        return JsonResponse({'status': 0,
                             'message': '没有此用户'})

@csrf_exempt
def profile_change(request):
    username = request.POST.get('username')
    user_obj = models.User.objects.filter(username=username)
    email = request.POST.get('email')
    img = request.POST.get('img')
    img = img.split(',')[1].encode(encoding='UTF-8')
    if email != '' and img == '':
        user_obj.update(email=email)
        return JsonResponse({'status': 1,
                             'message': '修改成功'})
    elif email == '' and img != '':
        img_name = f'{uuid.uuid4().hex[:8]}.jpg'
        img_path = username + '/' + img_name
        with open(os.path.join(MEDIA_ROOT, img_path), 'wb') as f:
            f.write(base64.b64decode(img))
        user_obj.update(avatar=img_path)
        return JsonResponse({'status': 1,
                             'message': '修改成功',
                             'data': {
                                 'avatar': img_path
                             }})
    else:
        # 去除data:image/jpeg;base64, 并编码成bytes类型
        img_name = f'{uuid.uuid4().hex[:8]}.jpg'
        img_path = username + '/' + img_name
        with open(os.path.join(MEDIA_ROOT, img_path), 'wb') as f:
            f.write(base64.b64decode(img))
        user_obj.update(email=email, avatar=img_path)
        return JsonResponse({'status': 1,
                             'message': '修改成功',
                             'data': {
                                 'avatar': img_path
                             }})
