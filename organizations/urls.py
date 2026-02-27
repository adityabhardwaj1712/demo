from django.urls import path
from . import html_views
from .views import (
    OrganizationListCreateView,
    OrganizationMembersView,
    AddMemberView,
)

urlpatterns = [

    path("page/", html_views.organizations_page, name="organizations_page"),
    path("delete/<int:pk>/", html_views.delete_organization, name="delete_organization"),
    path("add-member/<int:org_id>/", html_views.add_member, name="add_member"),

    path("api/", OrganizationListCreateView.as_view(), name="organization_list_create"),
    path("api/<int:pk>/members/", OrganizationMembersView.as_view(), name="organization_members"),
    path("api/<int:pk>/add-member/", AddMemberView.as_view(), name="organization_add_member_api"),
]