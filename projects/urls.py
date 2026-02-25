from django.urls import path
from .views import (
    ProjectListCreateView,
    TaskListCreateView,
    CommentCreateView,
)

urlpatterns = [
    path("", ProjectListCreateView.as_view()),
    path("<int:project_id>/tasks/", TaskListCreateView.as_view()),
    path("tasks/<int:task_id>/comments/", CommentCreateView.as_view()),
]