from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "project", "message", "is_read", "created_at")
    list_filter = ("is_read", "project")
    search_fields = ("recipient__username", "message")