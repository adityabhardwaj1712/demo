from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


@shared_task
def create_notification(user_id, message):
    try:
        user = User.objects.get(id=user_id)

        Notification.objects.create(
            user=user,
            message=message
        )

        print(f"Notification created for user {user.username}")

    except User.DoesNotExist:
        print(f"User with id {user_id} not found")