from django.contrib import admin
from .models import Project, Task, Comment, ActivityLog

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(ActivityLog)