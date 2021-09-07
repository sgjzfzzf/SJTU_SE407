from django.urls import path

from . import views

urlpatterns = [
    path('course/<str:course_id>', views.getCoursePage,
         name="course_page"),  # 用于访问目标课程的URL，参数为课程号
    path('getteachercoursepage/<str:course_id>/<str:teacher_name>',
         views.getTeacherCoursePage, name="get_teacher_course_page"),  # 用于Ajax刷新教师有关信息的URL
    path('submitcomment/<str:course_id>', views.submitComment,
         name="submit_comment"),  # 提交评论用URL
    path('deletecomment/<str:comment_id>',
         views.deleteComment, name="delete_comment"),
    path('addLike/<int:comment_id>', views.addLike,
         name="add_like"),  # 点赞用URL，参数为评论的id
    path('deleteLike/<int:comment_id>', views.deleteLike,
         name="delete_like"),  # 取消赞用URL，参数为评论的id
    path('sendMessage/<int:comment_id>', views.sendMessage, name="send_message"),
    path('readMessageSender/<int:comment_id>', views.readMessageSender, name="read_message_sender"),
    path('search/', views.searchPage, name="search_main_page"),
    path('searchResult/', views.searchResult, name="search_result"),
    path('searchlist', views.searchlist, name="searchlist"),
    path('searchlist/result', views.searchlistresult, name="searchlist_result"),
    path('', views.searchPage, name='home'),  # 登录，默认访问 127.0.0.1:8000 时展示登录界面
]
