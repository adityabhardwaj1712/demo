from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Notification.objects.filter(
            recipient=request.user
        ).order_by("-created_at")

        return Response(
            NotificationSerializer(qs, many=True).data
        )


class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            notification = Notification.objects.get(
                pk=pk,
                recipient=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True
        notification.save()

        return Response({"status": "ok"})