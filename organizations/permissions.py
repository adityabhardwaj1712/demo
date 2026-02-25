from .models import Membership


def is_org_admin(user, organization_id):
    return Membership.objects.filter(
        user=user,
        organization_id=organization_id,
        role="admin",
    ).exists()