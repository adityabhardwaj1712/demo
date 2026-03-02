from django.contrib import admin
from .models import Project, Task, Comment, ActivityLog


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status")
    list_filter = ("status", "project")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "user", "created_at")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "user", "action", "created_at")