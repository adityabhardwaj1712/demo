from django.urls import path
from .views import (
    ProjectListCreateView,
    TaskListCreateView,
    CommentCreateView,
)
from .html_views import (
    dashboard,
    projects_page,
    delete_project,
    tasks_page,
    delete_task,
    comments_page,
    delete_comment,
    activity_logs_page,
)

urlpatterns = [

    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),

    # Projects
    path("page/", projects_page, name="projects_page"),
    path("delete/<int:pk>/", delete_project, name="delete_project"),

    # Tasks
    path("tasks/", tasks_page, name="tasks_page"),
    path("tasks/delete/<int:pk>/", delete_task, name="delete_task"),

    # Comments
    path("comments/", comments_page, name="comments_page"),
    path("comments/delete/<int:pk>/", delete_comment, name="delete_comment"),

    # Activity
    path("activity/", activity_logs_page, name="activity_logs_page"),

    # API
    path("api/", ProjectListCreateView.as_view()),
    path("api/<int:project_id>/tasks/", TaskListCreateView.as_view()),
    path("api/tasks/<int:task_id>/comments/", CommentCreateView.as_view()),
]