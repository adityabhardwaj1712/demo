from django.urls import path
from .views import (
    OrganizationListCreateView,
    OrganizationMembersView,
    AddMemberView,
)
from .html_views import organizations_page, delete_organization

urlpatterns = [

    # HTML
    path("page/", organizations_page, name="organizations_page"),
    path("delete/<int:pk>/", delete_organization, name="delete_organization"),

    # API
    path("", OrganizationListCreateView.as_view(), name="org_list_create"),
    path("<int:org_id>/members/", OrganizationMembersView.as_view(), name="org_members"),
    path("<int:org_id>/add-member/", AddMemberView.as_view(), name="org_add_member"),
]