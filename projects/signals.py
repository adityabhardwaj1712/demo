from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Comment, ActivityLog
from notifications.tasks import create_notification


@receiver(post_save, sender=Task)
def task_activity(sender, instance, created, **kwargs):
    action = "created task" if created else "updated task"

    ActivityLog.objects.create(
        user=instance.assignee,
        project=instance.project,
        action=f"{action}: {instance.title}",
    )

    if instance.assignee:
        create_notification.delay(
            instance.assignee.id,
            f"Task '{instance.title}' was {action}",
        )


@receiver(post_save, sender=Comment)
def comment_activity(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            user=instance.user,
            project=instance.task.project,
            action="commented on a task",
        )

        if instance.task.assignee:
            create_notification.delay(
                instance.task.assignee.id,
                "New comment on your task",
            )