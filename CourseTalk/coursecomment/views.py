
from account.models import *
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.template import Context, Template
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import *

# Create your views here.
# 登录模块完成后添加对各种操作的用户权限进行检查的功能


@login_required
@require_http_methods(['GET'])
def getCoursePage(request, course_id):
    # 初始化课程界面
    user = request.user
    try:
        course = Course.objects.filter(course_id=course_id)[0]
    except IndexError:
        return render(request, 'coursecomment/CourseNotFoundPage.html')
    course.teacher = None
    comments = Comment.objects.filter(course__course_id=course_id)
    comments = sorted(
        comments, key=lambda comment: comment.total_likes())[::-1]
    # 这个列表的每一项存放一个字典，其中'comment_obj'项存储Comment对象，'is_liked'表示目前用户是否已经点赞过了，以此决定点赞按钮的样式
    comments_info = list()
    for comment in comments:
        comment_info = dict()
        comment_info['comment_obj'] = comment
        try:
            like = Like.objects.get(user=user, comment=comment)
        except Like.DoesNotExist:
            comment_info['is_liked'] = "Like"
        else:
            comment_info['is_liked'] = "Liked"
        if comment.user == user:
            comment_info['is_user'] = True
        else:
            comment_info['is_user'] = False
        comments_info.append(comment_info)
    teachers = [course.teacher for course in Course.objects.filter(
        course_id=course_id)]
    # revised by SEA_HORIZON,分页显示评论的具体内容
    object_list = comments_info
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'coursecomment/CoursePage.html', {'course': course, "teachers": teachers, "comments_info": posts, 'page': page})


@login_required
@require_http_methods(['GET'])
def getTeacherCoursePage(request, course_id, teacher_name):
    # 实现选择教师后课程界面的刷新
    user = request.user
    if teacher_name == "None":
        course = get_list_or_404(Course, course_id=course_id)[0]
        course.teacher = None
        comments = Comment.objects.filter(
            course__course_id=course_id)
        comments = sorted(
            comments, key=lambda comment: comment.total_likes())[::-1]
    else:
        course = get_object_or_404(
            Course, course_id=course_id, teacher__teacher_name=teacher_name)
        comments = Comment.objects.filter(
            course__course_id=course_id, course__teacher__teacher_name=teacher_name)
        comments = sorted(
            comments, key=lambda comment: comment.total_likes())[::-1]
    comments_info = list()
    for comment in comments:
        comment_info = dict()
        comment_info['comment_obj'] = comment
        if len(Like.objects.filter(user=user, comment=comment)) == 0:
            comment_info['is_liked'] = "Like"
        else:
            comment_info['is_liked'] = "Liked"
        if comment.user == user:
            comment_info['is_user'] = True
        else:
            comment_info['is_user'] = False
        comments_info.append(comment_info)
    # 返回渲染完成后的评论区HTML代码到JavaScript文件中
    return render(request, 'coursecomment/CommentsTemplate.html', {'course': course, "comments_info": comments_info})


@login_required
@require_http_methods(['POST'])
def submitComment(request, course_id):
    # 提交评论用函数
    user = request.user
    teacher_name = request.POST.get("teacher_name")
    comment_text = request.POST.get("comment_text")
    course_time = request.POST.get("course_time")
    course_score = eval(request.POST.get("course_score"))
    course_mark = eval(request.POST.get("course_mark"))
    if course_score <= 100 and course_score >= 0 and course_mark <= 10 and course_mark >= 0:
        comment = Comment.objects.create(
            user=user, course=Course.objects.get(course_id=course_id, teacher__teacher_name=teacher_name), course_time=course_time, course_score=course_score, course_mark=course_mark, comment_text=comment_text)
        comment.save()
        return redirect(reverse("course_page", kwargs={'course_id': course_id, }))
    else:
        raise Http404()


@login_required
@require_http_methods(['GET'])
def deleteComment(request, comment_id):
    # 删除目标评论
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExsit:
        return render(request, 'coursecomment/ErrorPage.html')
    else:
        if request.user == comment.user:
            comment.delete()
            course_id = comment.course.course_id
            return redirect(reverse("course_page", kwargs={'course_id': course_id, }))
        else:
            raise Http404()


@login_required
@require_http_methods(['GET'])
def addLike(request, comment_id):
    # 点赞用函数
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    try:
        like = Like.objects.create(user=user, comment=comment)
    except IntegrityError:
        raise Http404()
    like.save()
    return HttpResponse(str(len(Like.objects.filter(comment=comment))))


@login_required
@require_http_methods(['GET'])
def deleteLike(request, comment_id):
    # 取消赞用函数
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    like = get_object_or_404(Like, user=user, comment=comment)
    like.delete()
    return HttpResponse(str(len(Like.objects.filter(comment=comment))))


@login_required
@require_http_methods(['POST'])
def sendMessage(request, comment_id):
    # 发送私信用函数
    text = request.POST.get('message_text')
    isSender = bool(int(request.POST.get('isSender')))
    related_comment = get_object_or_404(Comment, pk=comment_id)
    if isSender:
        receiver = related_comment.user
    else:
        receiver_username = request.POST.get('user')
        receiver = get_object_or_404(User, username=receiver_username)
    message = Message.objects.create(
        sender=request.user, receiver=receiver, related_comment=related_comment, text=text)
    message.save()
    if isSender:
        return redirect(reverse("read_message_sender", kwargs={"comment_id": comment_id, }))
    else:
        return redirect(reverse("read_message_receiver", kwargs={"comment_id": comment_id, }))


@login_required
@require_http_methods(['GET', 'POST'])
def readMessageSender(request, comment_id):
    # 发信者阅读私信用
    messages = Message.objects.filter(Q(sender=request.user, related_comment__id=comment_id) | Q(
        receiver=request.user, related_comment__id=comment_id)).order_by('sendtime')
    for message in messages:
        if message.receiver == request.user:
            message.haveread = True
            message.save()
    return render(request, 'coursecomment/MessagesPageSender.html', {'messages': messages, 'comment_id': comment_id})


@login_required
def searchPage(request):
    # 搜索页面函数
    return render(request, 'coursecomment/CourseSearchPage.html')


@login_required
def searchResult(request):
    # 搜索函数
    q = request.GET.get('result')
    context = None
    if q:
        compound = ''
        tmp = []
        for i in range(len(q)):
            tmp.append('%')
            tmp.append(q[i])
        tmp.append('%')
        compound = compound.join(tmp)
        c = {}
        # 向用户输入中加入%转化为可以模糊化查询的字符串
        roughsearch = Course.objects.raw(
            "SELECT * FROM coursecomment_course WHERE course_name LIKE %s OR course_id LIKE %s", [compound, compound])
        name_list = []
        result_list = []
        for c in roughsearch:
            if not c.course_name in name_list:
                name_list.append(c.course_name)
                result_list.append(c)
        context = {'result_list': result_list, 'name_list': name_list}
    return render(request, 'coursecomment/SearchResultPage.html', context)


@login_required
def searchlist(request):
    head = 'search'
    colleage_list = []
    credits_list = []
    for course in Course.objects.all():
        colleage_list.append(course.course_colleage)
    colleages = sorted(list(set(colleage_list)))
    for course in Course.objects.all():
        credits_list.append(course.course_credit)
    credits = sorted(list(set(credits_list)))
    return render(request, 'coursecomment/Searchlist.html', {"head": head, "colleages": colleages, "credits": credits})


@login_required
def searchlistresult(request):
    search_colleage = request.POST.get('colleage')
    search_credit = request.POST.get('credit')
    search_type = request.POST.get('type')
    search_order = request.POST.get('order')
    # 用一个字典保存前端发送的条件
    search_dict = {}
    if search_colleage != "全部":
        search_dict['course_colleage'] = search_colleage
    if search_credit != "全部":
        search_dict['course_credit'] = search_credit
    if search_type != "全部":
        search_dict['course_type'] = search_type
    # 查询
    course_list = list()
    course_list_origin = Course.objects.filter(**search_dict)
    for course in course_list_origin:
        if course.course_id not in map(lambda course: course.course_id, course_list):
            course_list.append(course)
    # 排序
    if search_order == "按照平均成绩从大到小":
        course_list = sorted(
            course_list, key=lambda a: a.average_score(), reverse=True)
    elif search_order == "按照平均评分从大到小":
        course_list = sorted(
            course_list, key=lambda a: a.comment_mark(), reverse=True)
    return render(request, 'coursecomment/Searchlistresult.html', {'course_list': course_list})
