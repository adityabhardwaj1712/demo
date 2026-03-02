from django.db import models
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=255)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_organizations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Membership(models.Model):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("developer", "Developer"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"