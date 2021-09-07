from account.models import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from account.models import *

# Create your models here.


class Teacher(models.Model):
    # 授课老师的信息储存
    teacher_name = models.CharField(max_length=20, primary_key=True)  # 授课教师姓名
    teacher_contact = models.EmailField()  # 授课教师联系方式

    def __str__(self):
        return self.teacher_name


class Course(models.Model):
    # 课程信息储存
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 授课教师对象
    course_id = models.CharField(max_length=20)  # 课程号
    course_name = models.CharField(max_length=20)  # 课程名
    course_colleage = models.CharField(max_length=20)  # 开课学院
    course_credit = models.IntegerField()  # 课程学分
    course_type = models.CharField(max_length=20)  # 课程类型

    class Meta:
        # ('course_id','teacher')元组为唯一值的约束
        unique_together = (('course_id', 'teacher',),)

    def __str__(self):
        return str(self.course_id)

    def comment_mark(self):
        # 返回对一门课程的平均评分
        courses = Course.objects.filter(course_id=self.course_id)
        mark = 0
        comment_num = 0
        for course in courses:
            for comment in course.comment_set.all():
                try:
                    weight = comment.user.profile_set.all()[
                        0].get_mark_weight()
                except IndexError:
                    return 0
                mark += comment.course_mark*weight
                comment_num += weight
        if comment_num == 0:
            return 0
        else:
            return round(mark / comment_num, 2)

    def teacher_comment_mark(self):
        # 返回对某一位老师一门课程的平均评分
        comments = self.comment_set.all()
        if len(comments) == 0:
            return 0
        else:
            mark = 0
            comment_num = 0
            for comment in comments:
                try:
                    weight = comment.user.profile_set.all()[
                        0].get_mark_weight()
                except IndexError:
                    return 0
                mark += comment.course_mark*weight
                comment_num += weight
            return round(mark / comment_num, 2)

    def average_score(self):
        # 返回某一门课程的平均成绩
        courses = Course.objects.filter(course_id=self.course_id)
        score = 0
        comment_num = 0
        for course in courses:
            for comment in course.comment_set.all():
                score += comment.course_score
                comment_num += 1
        if comment_num == 0:
            return 0
        else:
            return round(score / comment_num, 2)

    def teacher_average_score(self):
        # 返回某一位老师教授某一门课程的平均成绩
        comments = self.comment_set.all()
        if len(comments) == 0:
            return 0
        else:
            score = 0
            for comment in comments:
                score += comment.course_score
            return round(score / len(comments), 2)


class Comment(models.Model):
    # 存储评论信息
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 发出评论的用户对象
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 评论的课程对象
    course_time = models.DateField()  # 授课时间
    course_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])  # 课程最终得分，指评论用户的得分
    course_mark = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])  # 对课程的评分
    comment_text = models.TextField()  # 对课程的文字评价
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间，已设置自动添加

    def __str__(self):
        return str(self.comment_text)

    def total_likes(self):
        # 返回一条评论的所有点赞数
        likes = self.like_set.all()
        return len(likes)


class Like(models.Model):
    # 赞的对象，引入这个对象是为了防止一条评论多个用户点赞的情况出现
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'comment',),)

    def __str__(self):
        return "{}:{}".format(self.user.username, self.comment.comment_text)


class Message(models.Model):
    # 私信对象
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")  # 发送私信的用户
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver")
    related_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE)  # 关联的评论
    text = models.TextField()  # 私信内容
    sendtime = models.DateTimeField(auto_now_add=True)  # 私信发送时间
    haveread = models.BooleanField(default=False)  # 标记是否是已读消息

    def __str__(self):
        return self.text
