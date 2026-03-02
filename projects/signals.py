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

    # FIX: use assigned_to instead of assignee
    if instance.assigned_to:
        ActivityLog.objects.create(
            user=instance.assigned_to,
            project=instance.project,
            action=f"{action} task: {instance.title}",
        )

        try:
            create_notification.delay(
                instance.assigned_to.id,
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

        # FIX: use assigned_to instead of assignee
        if (
            instance.task.assigned_to
            and instance.task.assigned_to != instance.user
        ):
            try:
                create_notification.delay(
                    instance.task.assigned_to.id,
                    f"New comment on task '{instance.task.title}'",
                )
            except Exception as e:
                print("Celery error (comment notification):", e)