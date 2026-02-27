from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Comment, ActivityLog
from notifications.tasks import create_notification


@receiver(post_save, sender=Task)
def task_activity(sender, instance, created, **kwargs):
    """
    Handles activity logging and notifications when a Task
    is created or updated.
    """

    action = "created" if created else "updated"

    if instance.assignee:
        ActivityLog.objects.create(
            user=instance.assignee,
            project=instance.project,
            action=f"{action} task: {instance.title}",
        )

        try:
            create_notification.delay(
                instance.assignee.id,
                f"Task '{instance.title}' was {action}",
            )
        except Exception as e:
            print("Celery error (task notification):", e)


@receiver(post_save, sender=Comment)
def comment_activity(sender, instance, created, **kwargs):
    """
    Handles activity logging and notifications
    when a Comment is created.
    """

    if created:
        ActivityLog.objects.create(
            user=instance.user,
            project=instance.task.project,
            action=f"commented on task: {instance.task.title}",
        )

        if (
            instance.task.assignee
            and instance.task.assignee != instance.user
        ):
            try:
                create_notification.delay(
                    instance.task.assignee.id,
                    f"New comment on task '{instance.task.title}'",
                )
            except Exception as e:
                print("Celery error (comment notification):", e)