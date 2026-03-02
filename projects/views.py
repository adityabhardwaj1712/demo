from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Prefetch
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from organizations.models import Membership


def get_user_membership(user):
    return Membership.objects.filter(user=user).select_related("organization").first()


# --------------------------------------------------
# PROJECT LIST
# --------------------------------------------------
@login_required
def project_list(request):
    membership = get_user_membership(request.user)

    if not membership:
        return render(request, "projects/project_list.html", {
            "projects": [],
            "form": None,
            "role": None
        })

    projects = Project.objects.filter(
        organization=membership.organization
    ).select_related("organization", "created_by")

    # Only admin can create project
    if request.method == "POST":
        if membership.role != "admin":
            return HttpResponseForbidden("You don't have permission.")

        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.organization = membership.organization
            project.created_by = request.user
            project.save()
            return redirect("project_list")
    else:
        form = ProjectForm() if membership.role == "admin" else None

    return render(request, "projects/project_list.html", {
        "projects": projects,
        "form": form,
        "role": membership.role
    })


# --------------------------------------------------
# TASK BOARD (KANBAN)
# --------------------------------------------------
@login_required
def task_board(request, project_id):
    membership = get_user_membership(request.user)

    if not membership:
        return HttpResponseForbidden("No organization access.")

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=membership.organization
    )

    tasks = Task.objects.filter(
        project=project
    ).select_related("assigned_to", "created_by")

    return render(request, "projects/board.html", {
        "project": project,
        "todo": tasks.filter(status="todo"),
        "progress": tasks.filter(status="in_progress"),
        "done": tasks.filter(status="done"),
        "role": membership.role
    })


# --------------------------------------------------
# CREATE TASK
# --------------------------------------------------
@login_required
def create_task(request, project_id):
    membership = get_user_membership(request.user)

    if not membership:
        return HttpResponseForbidden("No organization access.")

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=membership.organization
    )

    # Viewer cannot create task
    if membership.role == "viewer":
        return HttpResponseForbidden("You don't have permission.")

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            return redirect("task_board", project_id=project.id)
    else:
        form = TaskForm()

    return render(request, "projects/create_task.html", {
        "form": form,
        "project": project
    })