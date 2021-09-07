from django.test import TestCase
from .models import *
from math import exp
from django.contrib.auth.models import User

#models生成函数,方便生成相应的集,并且可以用默认值生成模型
def create_teacher(name="wang",contact="123456"):
    return Teacher.objects.create(teacher_name=name,teacher_contact=contact)

def create_user(username="user1",userpassword="123456",useremail="123456@qq.com",usersex="男"):
    return User.objects.create(name=username,password=userpassword,email=useremail,sex=usersex)

def create_course(teachername="wang",teachercontact="123456",courseid="MA1",coursename="高等数学",coursecolleage="数学学院",coursecredit=3,coursetype="必修课"):
    create_teacher(teachername,teachercontact)
    teacher1=Teacher.objects.get(teacher_name=teachername)
    return Course.objects.create(teacher=teacher1,course_id=courseid,course_name=coursename,course_colleage=coursecolleage,course_credit=coursecredit,course_type=coursetype)
    
#对models测试
class Teacher_test(TestCase):  #对teacher模型中函数进行测试
    def setUp(self) :
        create_teacher("wang","123456")

    def test_name(self):    #对_str_()函数进行测试
        teacher1=Teacher.objects.get(teacher_name="wang")
        self.assertEqual(teacher1.__str__(),"wang")

class Course_test(TestCase):    #对Course中函数测试
    def setUp(self) :    
        create_course()
        
    def test_str(self):  #对_str_()函数进行测试
        ma1=Course.objects.get(course_id="MA1")
        self.assertEqual(ma1.__str__(),"MA1")

class CourseTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user("user1")
        user2 = User.objects.create_user("user2")
        user3 = User.objects.create_user("user3")  # 创建测试用户
        userinfo1 = UserInfo.objects.create(user=user1)
        userinfo2 = UserInfo.objects.create(user=user2)
        userinfo3 = UserInfo.objects.create(user=user3)  # 关联测试用户信息
        teacher1 = Teacher.objects.create(
            teacher_name="李华", teacher_contact="00001@126.com")
        teacher2 = Teacher.objects.create(
            teacher_name="张三", teacher_contact="00002@126.com")
        teacher3 = Teacher.objects.create(
            teacher_name="李四", teacher_contact="00003@126.com")
        teacher4 = Teacher.objects.create(
            teacher_name="王五", teacher_contact="00004@126.com")  # 创建测试教师
        course1 = Course.objects.create(teacher=teacher1, course_id="A1", course_name="软件工程",
                                        course_colleage="电子信息与电气工程学院", course_credit=1, course_type="必修课")
        course2 = Course.objects.create(teacher=teacher2, course_id="A2", course_name="数据库原理",
                                        course_colleage="电子信息与电气工程学院", course_credit=2, course_type="选修课")
        course3 = Course.objects.create(teacher=teacher3, course_id="A3", course_name="高等数学",
                                        course_colleage="数学科学学院", course_credit=6, course_type="必修课")
        course4 = Course.objects.create(teacher=teacher4, course_id="A4", course_name="信号与系统",
                                        course_colleage="电子信息与电气工程学院", course_credit=3, course_type="必修课")
        course5 = Course.objects.create(teacher=teacher1, course_id="A4", course_name="信号与系统",
                                        course_colleage="电子信息与电气工程学院", course_credit=3, course_type="必修课")
        # 创建测试用课程
        comment1 = Comment.objects.create(user=user1, course=course1, course_time='2018-08-30', course_score=89,
                                          course_mark=6, comment_text="nice")
        comment2 = Comment.objects.create(user=user2, course=course1, course_time='2018-08-30', course_score=92,
                                          course_mark=8, comment_text="nice")
        comment3 = Comment.objects.create(user=user3, course=course1, course_time='2018-08-30', course_score=95,
                                          course_mark=9, comment_text="nice")
        # 创建测试用课程1的评论
        comment4 = Comment.objects.create(user=user1, course=course2, course_time='2018-08-30', course_score=85,
                                          course_mark=7, comment_text="nice")
        comment5 = Comment.objects.create(user=user2, course=course2, course_time='2018-08-30', course_score=88,
                                          course_mark=9, comment_text="nice")
        # 创建测试用课程2的评论

        comment6 = Comment.objects.create(user=user2, course=course3, course_time='2018-08-30', course_score=91,
                                          course_mark=8, comment_text="good")
        comment7 = Comment.objects.create(user=user3, course=course3, course_time='2018-09-30', course_score=92,
                                          course_mark=5, comment_text="well")

        # 创建测试用课程3的评论

        comment8 = Comment.objects.create(user=user1, course=course4, course_time='2018-09-30', course_score=87,
                                          course_mark=9, comment_text="有点难")
        # 创建测试用课程4教师4的评论
        comment9 = Comment.objects.create(user=user3, course=course5, course_time='2018-09-30', course_score=77,
                                          course_mark=7, comment_text="有点难")

        # 创建测试用课程4教师1的评论
        like = Like.objects.create(user=user1, comment=comment1)
        like = Like.objects.create(user=user2, comment=comment1)
        like = Like.objects.create(user=user3, comment=comment1)
        like = Like.objects.create(user=user1, comment=comment2)
        like = Like.objects.create(user=user2, comment=comment2)
        like = Like.objects.create(user=user3, comment=comment3)
        # 添加测试用评论点赞


    def test_1(self):
        userinfo1 = UserInfo.objects.get(pk=1)
        userinfo2 = UserInfo.objects.get(pk=2)
        userinfo3 = UserInfo.objects.get(pk=3)  # 关联测试用户信息
        user1_mark_weight = 2 - 2 * exp(-6)
        user2_mark_weight = 2 - 2 * exp(-5)
        user3_mark_weight = 2 - 2 * exp(-4)  # 直接计算用户对课程评价的权重分
        self.assertEqual(userinfo1.get_mark_weight(), user1_mark_weight)
        self.assertEqual(userinfo2.get_mark_weight(), user2_mark_weight)
        self.assertEqual(userinfo3.get_mark_weight(),
                         user3_mark_weight)  # 测试计算用户对课程评价的权重分
    def test_2(self):
        course1 = Course.objects.get(pk=1)
        course2 = Course.objects.get(pk=2)
        course3 = Course.objects.get(pk=3)
        course4 = Course.objects.get(pk=4)
        course5 = Course.objects.get(pk=5)
        user1_mark_weight = 2 - 2 * exp(-6)
        user2_mark_weight = 2 - 2 * exp(-5)
        user3_mark_weight = 2 - 2 * exp(-4)  # 直接计算用户对课程评价的权重分
        self.assertEqual(course1.comment_mark(), round(
            (6 * user1_mark_weight + 8 * user2_mark_weight + 9 * user3_mark_weight)
            / (user1_mark_weight + user2_mark_weight + user3_mark_weight), 2))
        self.assertEqual(course2.comment_mark(), round(
            (7 * user1_mark_weight + 9 * user2_mark_weight) / (user1_mark_weight + user2_mark_weight), 2))
        self.assertEqual(course3.comment_mark(), round(
            (8 * user2_mark_weight + 5 * user3_mark_weight) / (user2_mark_weight + user3_mark_weight), 2))
        self.assertEqual(course4.comment_mark(), round(
            (9 * user1_mark_weight + 7 * user3_mark_weight) / (user1_mark_weight + user3_mark_weight), 2))
        # 测试课程平均评分
        self.assertEqual(course1.teacher_comment_mark(), round(
            (6 * user1_mark_weight + 8 * user2_mark_weight + 9 * user3_mark_weight)
            / (user1_mark_weight + user2_mark_weight + user3_mark_weight), 2))
        self.assertEqual(course2.teacher_comment_mark(), round(
            (7 * user1_mark_weight + 9 * user2_mark_weight) / (user1_mark_weight + user2_mark_weight), 2))
        self.assertEqual(course3.teacher_comment_mark(), round(
            (8 * user2_mark_weight + 5 * user3_mark_weight) / (user2_mark_weight + user3_mark_weight), 2))
        self.assertEqual(course4.teacher_comment_mark(), 9)
        self.assertEqual(course5.teacher_comment_mark(), 7)
        # 测试教师对应课程平均评分
    def test_3(self):
        course1 = Course.objects.get(pk=1)
        course2 = Course.objects.get(pk=2)
        course3 = Course.objects.get(pk=3)
        course4 = Course.objects.get(pk=4)
        course5 = Course.objects.get(pk=5)
        self.assertEqual(course1.average_score(), 92)
        self.assertEqual(course2.average_score(), 86.5)
        self.assertEqual(course3.average_score(), 91.5)
        self.assertEqual(course4.average_score(), 82)
        # 测试课程平均成绩
        self.assertEqual(course1.teacher_average_score(), 92)
        self.assertEqual(course2.teacher_average_score(), 86.5)
        self.assertEqual(course3.teacher_average_score(), 91.5)
        self.assertEqual(course4.teacher_average_score(), 87)
        self.assertEqual(course5.teacher_average_score(), 77)
        # 测试教师对应课程平均成绩
    def test_4(self):
        comment1 = Comment.objects.get(pk=1)
        comment2 = Comment.objects.get(pk=2)
        comment3 = Comment.objects.get(pk=3)
        comment4 = Comment.objects.get(pk=4)
        comment5 = Comment.objects.get(pk=5)
        comment6 = Comment.objects.get(pk=6)
        comment7 = Comment.objects.get(pk=7)
        comment8 = Comment.objects.get(pk=8)
        comment9 = Comment.objects.get(pk=9)
        self.assertIsInstance(comment1.total_likes(), int)
        self.assertEqual(comment1.total_likes(), 3)
        self.assertEqual(comment2.total_likes(), 2)
        self.assertEqual(comment3.total_likes(), 1)
        self.assertEqual(comment4.total_likes(), 0)
        self.assertEqual(comment5.total_likes(), 0)
        self.assertEqual(comment6.total_likes(), 0)
        self.assertEqual(comment7.total_likes(), 0)
        self.assertEqual(comment8.total_likes(), 0)
        self.assertEqual(comment9.total_likes(), 0)
        # 测试评论点赞数
