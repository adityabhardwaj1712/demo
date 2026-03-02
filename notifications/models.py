from django.db import models
from django.conf import settings


class Notification(models.Model):

    TYPE_CHOICES = [
        ("task_assigned", "Task Assigned"),
        ("task_updated", "Task Updated"),
        ("comment_added", "Comment Added"),
        ("project_created", "Project Created"),
        ("system", "System"),
    ]

    # Who receives it
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    # Who triggered it
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="triggered_notifications"
    )

    # Multi-tenant support
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    # Type of notification
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default="system"
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.recipient.email} - {self.notification_type}"