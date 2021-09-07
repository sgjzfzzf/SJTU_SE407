from coursecomment.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import *
from .models import Profile

# Create your views here.


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form': user_form})


def dashboard(request):
    name = request.user.username
    q = name
    if q:
        result_list = Comment.objects.filter(user__username=q)
    return render(request, 'account/dashboard.html', {'user': request.user, 'name': name, 'result_list': result_list})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    print("hello, world")
                    login(request, user)
                    return HttpResponse('Authenticated ''successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':  # 分成提交表单和填写表单两个分支，在模板里面进一步处理
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])  # 对用户提交的密码进行hash加密
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@require_http_methods(['GET'])
@login_required
def readMessageBox(request):
    # 生成私信箱页面
    comments = Comment.objects.filter(Q(user=request.user) | Q(
        message__sender=request.user)).distinct()
    messages_list = list()
    for comment in comments:
        messages = Message.objects.filter(related_comment=comment)
        messages_dict = dict()
        messages_dict['comment'] = comment
        messages_dict['haveread'] = True
        messages_dict['isSender'] = (comment.user != request.user)
        for message in messages:
            if not message.haveread:
                messages_dict['haveread'] = False
                break
        messages_list.append(messages_dict)
    return render(request, 'account/MessageBox.html', {'messages_list': messages_list})


@require_http_methods(['GET'])
@login_required
def readMessageReceiver(request, comment_id):
    # 接收者阅读私信
    comment = get_object_or_404(Comment, pk=comment_id)
    messages = Message.objects.filter(related_comment=comment)
    messages_group = dict()
    for message in messages:
        if message.sender == request.user:
            if message.receiver not in messages_group.keys():
                messages_group[message.receiver] = list()
            messages_group[message.receiver].append(message)
        else:
            if message.receiver == request.user:
                message.haveread = True
                message.save()
            if message.sender not in messages_group.keys():
                messages_group[message.sender] = list()
            messages_group[message.sender].append(message)
    return render(request, 'account/MessagePageReceiver.html', {'messages_group': messages_group, 'comment_id': comment_id})
