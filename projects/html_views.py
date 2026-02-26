from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms

from organizations.models import Organization
from .models import Project, Task, Comment, ActivityLog


# =====================================================
# FORMS
# =====================================================

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "organization"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "project", "assignee", "status"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["task", "text"]   # ✅ FIXED HERE


# =====================================================
# DASHBOARD
# =====================================================

@login_required
def dashboard(request):
    orgs = Organization.objects.filter(owner=request.user)
    projects = Project.objects.filter(organization__owner=request.user)
    tasks = Task.objects.filter(assignee=request.user)

    return render(request, "dashboard.html", {
        "orgs": orgs,
        "projects": projects,
        "tasks": tasks,
    })


# =====================================================
# PROJECT CRUD
# =====================================================

@login_required
def projects_page(request):
    projects = Project.objects.filter(
        organization__owner=request.user
    )

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects_page")
    else:
        form = ProjectForm()

    return render(request, "projects.html", {
        "projects": projects,
        "form": form,
    })


@login_required
def delete_project(request, pk):
    project = get_object_or_404(
        Project,
        pk=pk,
        organization__owner=request.user
    )
    project.delete()
    return redirect("projects_page")


# =====================================================
# TASK CRUD
# =====================================================

@login_required
def tasks_page(request):
    tasks = Task.objects.filter(
        project__organization__owner=request.user
    )

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks_page")
    else:
        form = TaskForm()

    return render(request, "tasks.html", {
        "tasks": tasks,
        "form": form,
    })


@login_required
def delete_task(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        project__organization__owner=request.user
    )
    task.delete()
    return redirect("tasks_page")


# =====================================================
# COMMENT CRUD
# =====================================================

@login_required
def comments_page(request):
    comments = Comment.objects.filter(
        task__project__organization__owner=request.user
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("comments_page")
    else:
        form = CommentForm()

    return render(request, "comments.html", {
        "comments": comments,
        "form": form,
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(
        Comment,
        pk=pk,
        task__project__organization__owner=request.user
    )
    comment.delete()
    return redirect("comments_page")


# =====================================================
# ACTIVITY LOG VIEW
# =====================================================

@login_required
def activity_logs_page(request):
    logs = ActivityLog.objects.filter(
        project__organization__owner=request.user
    ).order_by("-created_at")

    return render(request, "activity_logs.html", {
        "logs": logs
    })