from math import exp
from django.db import models
from django.conf import settings
from coursecomment.models import *


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'UserInfo for user {self.user.username}'

    def get_mark_weight(self):
        # 计算用户对课程评价的权重分
        comments = Comment.objects.filter(user=self.user)
        total_likes = 0
        for comment in comments:
            total_likes += comment.total_likes()
        mark_weight = 2-2*exp(-(len(comments)+total_likes))
        return mark_weight

    def get_mark_weight(self):
        # 计算用户对课程评价的权重分
        comments = Comment.objects.filter(user=self.user)
        total_likes = 0
        for comment in comments:
            total_likes += comment.total_likes()
        mark_weight = 2-2*exp(-(len(comments)+total_likes))
        return mark_weight

# Create your models here.
