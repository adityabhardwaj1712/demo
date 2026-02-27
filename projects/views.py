from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from organizations.models import Membership


class ProjectListCreateView(APIView):
    """Show all projects the user belongs to + create a new one"""

    def get(self, request):
        projects = Project.objects.filter(
            organization__membership__user=request.user
        ).select_related("organization")

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        org_id = request.data.get("organization")

        if not org_id or not Membership.objects.filter(
            user=request.user,
            organization_id=org_id
        ).exists():
            return Response(
                {"detail": "You are not a member of this organization"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskListCreateView(APIView):
    """List tasks in one project + create new task"""

    def get(self, request, project_id):
        project = get_object_or_404(
            Project,
            id=project_id,
            organization__membership__user=request.user
        )

        tasks = Task.objects.filter(project=project).select_related(
            "assignee", "project"
        ).prefetch_related("comment_set")

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        project = get_object_or_404(
            Project,
            id=project_id,
            organization__membership__user=request.user
        )

        data = request.data.copy()
        data["project"] = project.id

        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentCreateView(APIView):
    """Add a comment to a task"""

    def post(self, request, task_id):
        task = get_object_or_404(
            Task,
            id=task_id,
            project__organization__membership__user=request.user
        )

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            task=task,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)