import os

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from myblog.settings import MEDIA_ROOT
from user.models import User
from blog.models import Blog, Tag, Comment, Reply


# 分页器
def paginate(blog_list, current_pages):
    paginator = Paginator(blog_list, 5)  # 实例化Paginator类
    num_pages = paginator.num_pages  # 可以分成几页
    blog_list = paginator.get_page(current_pages).object_list  # 当前页数的所有数据
    return {'data': blog_list, 'numPages': num_pages}


@csrf_exempt
def all_blog(request):
    blog_list = []
    current_pages = request.POST.get('currentPages')
    tag = request.POST.get('tag')
    if tag == 'undefined':
        blog_obj_list = Blog.objects.order_by('updated').reverse()
    else:
        tag_id = Tag.objects.get(name=tag).id
        blog_obj_list = Blog.objects.filter(tags=tag_id).order_by('updated').reverse()
    for blog_obj in blog_obj_list:
        blog_dict = {}
        tags = []
        tag_list = blog_obj.tags.all()
        for tag_obj in tag_list:
            tags.append(tag_obj.name)
        comment_list = blog_obj.comment_set.all()
        comment_num = len(comment_list)
        reply_num = 0
        for comment_obj in comment_list:
            reply_list = comment_obj.reply_set.all()
            reply_num += len(reply_list)
        blog_dict['id'] = blog_obj.id
        blog_dict['title'] = blog_obj.title
        blog_dict['content'] = blog_obj.content if len(blog_obj.content) <= 100 else (
                blog_obj.content[0: 100] + '...')
        blog_dict['author'] = blog_obj.user.username
        blog_dict['thumb'] = blog_obj.thumb
        blog_dict['visitNum'] = blog_obj.visit_num
        blog_dict['commentNum'] = comment_num + reply_num
        blog_dict['tags'] = tags
        blog_dict['created'] = blog_obj.created.strftime('%Y-%m-%d')
        blog_dict['updated'] = blog_obj.updated.strftime('%Y-%m-%d')
        blog_list.append(blog_dict)
    data = paginate(blog_list, current_pages)
    return JsonResponse({'status': 1, **data})

@csrf_exempt
def tags(request):
    tag_list = []
    tag_objs = Tag.objects.all()
    for tag_obj in tag_objs:
        tag = tag_obj.name
        tag_list.append(tag)
    return JsonResponse({'status': 1, 'data': tag_list})

@csrf_exempt
def blog(request):
    bid = request.POST.get('bid')
    blog_dict = {}
    blog_obj = Blog.objects.filter(id=bid)[0]
    visit_num = blog_obj.visit_num
    visit_num += 1
    Blog.objects.filter(id=bid).update(visit_num=visit_num)
    blog_dict['bid'] = blog_obj.id
    blog_dict['title'] = blog_obj.title
    blog_dict['author'] = blog_obj.user.username
    blog_dict['content'] = blog_obj.content
    blog_dict['visit_num'] = visit_num
    blog_dict['thumb'] = blog_obj.thumb
    blog_dict['created'] = blog_obj.created.strftime('%Y-%m-%d')
    blog_dict['updated'] = blog_obj.updated.strftime('%Y-%m-%d')
    tags = []
    tag_list = blog_obj.tags.all()
    for tag_obj in tag_list:
        tags.append(tag_obj.name)
    blog_dict['tags'] = tags
    return JsonResponse({'status': 1, 'data': blog_dict})

@csrf_exempt
def article_add(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    user = request.POST.get('user')
    # 博客数据库存放
    user_obj = User.objects.get(username=user)
    blog_obj = Blog.objects.create(title=title, content=content, user=user_obj)
    tag_list = request.POST.get('tags').split(',')
    for tag in tag_list:
        tag_obj = Tag.objects.filter(name=tag).first()
        if not tag_obj:
            tag_obj = Tag.objects.create(name=tag)
            tag_obj.save()
        blog_obj.tags.add(tag_obj)
    blog_obj.save()
    return JsonResponse({'status': 1,
                         'message': '发布成功'})

@csrf_exempt
def save_img(request):
    img_res = []
    # 博客图片存储
    img_list = request.FILES.getlist('imgList[]')
    for (index, img) in enumerate(img_list):
        print(index)
        img_url = []
        img_name = img.name
        img_path = os.path.join(MEDIA_ROOT + '/assets/', img_name)
        with open(img_path, 'wb') as f:
            for i in img.chunks():
                f.write(i)
        img_url.append(str(index + 1))
        img_url.append('assets/' + img_name)
        img_res.append(img_url)
    return JsonResponse({'status': 1,
                         'message': '图片上传成功',
                         'data': img_res})

@csrf_exempt
def show_comment(request):
    bid = request.POST.get('bid')
    comment_list = []
    blog_obj = Blog.objects.filter(id=bid)[0]
    comment_obj_list = blog_obj.comment_set.all()
    for comment_obj in comment_obj_list:
        reply_list = []
        reply_obj_list = comment_obj.reply_set.filter(comment_id=comment_obj.id)
        for reply_obj in reply_obj_list:
            reply_dict = {
                'id': reply_obj.id,
                'fromUser': reply_obj.from_uid.get().username,
                'toUser': User.objects.filter(id=reply_obj.to_uid)[0].username,
                'avatar': reply_obj.from_uid.get().avatar,
                'created': reply_obj.created.strftime('%Y-%m-%d %H:%M:%S'),
                'content': reply_obj.content,
            }
            reply_list.append(reply_dict)
        comment_dict = {
            'id': comment_obj.id,
            'fromUser': comment_obj.from_uid.get().username,
            'avatar': comment_obj.from_uid.get().avatar,
            'created': comment_obj.created.strftime('%Y-%m-%d %H:%M:%S'),
            'content': comment_obj.content,
            'replies': reply_list
        }
        comment_list.append(comment_dict)
    return JsonResponse({'status': 1, 'data': comment_list})

@csrf_exempt
def comment_add(request):
    content = request.POST.get('content')
    from_user = request.POST.get('fromUser')
    bid = request.POST.get('bid')
    from_uid = User.objects.get(username=from_user).id
    blog_obj = Blog.objects.get(id=bid)
    comment_obj = Comment.objects.create(
        content=content, bid=blog_obj
    )
    comment_obj.from_uid.add(from_uid)
    comment_obj.save()
    return JsonResponse({'status': 1, 'message': '评论成功'})

@csrf_exempt
def reply_add(request):
    reply_type = request.POST.get('type')
    cid = request.POST.get('cid')
    from_user = request.POST.get('fromUser')
    to_user = request.POST.get('toUser')
    content = request.POST.get('content')
    comment_obj = Comment.objects.get(id=cid)
    to_uid = User.objects.get(username=to_user).id
    from_uid = User.objects.get(username=from_user).id
    if reply_type == 'comment':
        reply_obj = Reply.objects.create(
            content=content, comment_id=comment_obj,
            to_uid=to_uid
        )
        reply_obj.from_uid.add(from_uid)
        reply_obj.save()
    elif reply_type == 'reply':
        rid = request.POST.get('rid')
        reply_obj = Reply.objects.create(
            content=content, comment_id=comment_obj, to_uid=to_uid,
            reply_id=Reply.objects.get(id=rid)
        )
        reply_obj.from_uid.add(from_uid)
        reply_obj.save()
    return JsonResponse({'status': 1, 'message': '回复成功'})
