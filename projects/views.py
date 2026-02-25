from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from organizations.models import Membership
from .models import Comment


class ProjectListCreateView(APIView):
    def get(self, request):
        projects = Project.objects.filter(
            organization__membership__user=request.user
        ).select_related("organization")

        return Response(ProjectSerializer(projects, many=True).data)

    def post(self, request):
        org_id = request.data.get("organization")

        if not Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
        ).exists():
            return Response({"detail": "Forbidden"}, status=403)

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response(serializer.data, status=201)


class TaskListCreateView(APIView):
    def get(self, request, project_id):
        tasks = Task.objects.filter(
            project_id=project_id
        ).select_related(
            "assignee",
            "project",
        ).prefetch_related("comment_set")

        return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request, project_id):
        if not Project.objects.filter(
            id=project_id,
            organization__membership__user=request.user,
        ).exists():
            return Response({"detail": "Forbidden"}, status=403)

        data = request.data.copy()
        data["project"] = project_id

        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(serializer.data, status=201)


class CommentCreateView(APIView):
    def post(self, request, task_id):
        if not Task.objects.filter(
            id=task_id,
            project__organization__membership__user=request.user,
        ).exists():
            return Response({"detail": "Forbidden"}, status=403)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(
            user=request.user,
            task_id=task_id,
        )
        return Response(serializer.data, status=201)