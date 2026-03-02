from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from organizations.models import Organization, Membership

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_workspace(sender, instance, created, **kwargs):
    if created:
        # Create personal workspace
        org = Organization.objects.create(
            name=f"{instance.username}'s Workspace",
            owner=instance
        )

        # Give admin role
        Membership.objects.create(
            user=instance,
            organization=org,
            role="admin"
        )