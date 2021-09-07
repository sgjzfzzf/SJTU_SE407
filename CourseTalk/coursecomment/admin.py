from django.contrib import admin

from .models import *

admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Teacher)
admin.site.register(Like)
admin.site.register(Message)
