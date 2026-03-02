from django.contrib import admin
from .models import Organization, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at")
    search_fields = ("name",)
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "organization", "role")
    list_filter = ("role",)