from django.urls import path
from .views import (
    OrganizationListCreateView,
    OrganizationMembersView,
    AddMemberView,
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view()),
    path("<int:org_id>/members/", OrganizationMembersView.as_view()),
    path("<int:org_id>/add-member/", AddMemberView.as_view()),
]