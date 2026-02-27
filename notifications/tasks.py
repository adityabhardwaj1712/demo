from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()


@shared_task
def create_notification(user_id, message, project_id=None):
    try:
        user = User.objects.get(id=user_id)

        notification = Notification.objects.create(
            recipient=user,
            message=message,
            project_id=project_id
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_notification",
                "data": {
                    "message": notification.message,
                    "id": notification.id,
                }
            }
        )

        print(f"Notification sent to {user.username}")

    except User.DoesNotExist:
        print(f"User with id {user_id} not found")