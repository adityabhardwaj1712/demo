from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser")
    search_fields = ("username", "email")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("job_title", "timezone")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("job_title", "timezone")}),
    )