from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from organizations.models import Membership
from .models import Project, Task, Comment, ActivityLog


# ==================================
# SIMPLE ROLE CHECK (NO EXTRA FILE)
# ==================================
def user_has_role(user, organization, roles):
    return Membership.objects.filter(
        user=user,
        organization=organization,
        role__in=roles
    ).exists()


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):

    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).distinct()

    tasks = Task.objects.filter(
        project__organization__memberships__user=request.user
    ).distinct()

    comments = Comment.objects.filter(
        task__project__organization__memberships__user=request.user
    ).distinct()

    return render(request, "dashboard.html", {
        "project_count": projects.count(),
        "task_count": tasks.count(),
        "comment_count": comments.count(),
    })


# =========================
# PROJECTS
# =========================
@login_required
def projects_page(request):

    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).distinct()

    return render(request, "projects.html", {
        "projects": projects
    })


@login_required
def project_detail(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if not Membership.objects.filter(
        user=request.user,
        organization=project.organization
    ).exists():
        return HttpResponseForbidden("Not allowed")

    tasks = Task.objects.filter(project=project)

    return render(request, "project_detail.html", {
        "project": project,
        "tasks": tasks
    })


@login_required
def delete_project(request, pk):

    project = get_object_or_404(Project, pk=pk)

    if not user_has_role(request.user, project.organization, ["admin"]):
        return HttpResponseForbidden("Not allowed")

    project.delete()

    return redirect("projects_page")


# =========================
# TASKS
# =========================
@login_required
def tasks_page(request):

    tasks = Task.objects.filter(
        project__organization__memberships__user=request.user
    ).distinct()

    return render(request, "tasks.html", {
        "tasks": tasks
    })


@login_required
def delete_task(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if not user_has_role(request.user, task.project.organization, ["admin"]):
        return HttpResponseForbidden("Not allowed")

    task.delete()

    return redirect("tasks_page")


# =========================
# COMMENTS
# =========================
@login_required
def comments_page(request):

    comments = Comment.objects.filter(
        task__project__organization__memberships__user=request.user
    ).distinct()

    return render(request, "comments.html", {
        "comments": comments
    })


@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    if not user_has_role(request.user, comment.task.project.organization, ["admin"]):
        return HttpResponseForbidden("Not allowed")

    comment.delete()

    return redirect("comments_page")


# =========================
# ACTIVITY LOGS
# =========================
@login_required
def activity_logs_page(request):

    logs = ActivityLog.objects.filter(
        project__organization__memberships__user=request.user
    ).order_by("-created_at")

    return render(request, "activity_logs.html", {
        "logs": logs
    })