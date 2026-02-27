from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django import forms
from django.contrib.auth import get_user_model

from .models import Organization, Membership
from notifications.tasks import create_notification

User = get_user_model()


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name"]


@login_required
def organizations_page(request):

    orgs = Organization.objects.filter(
        owner=request.user
    ).prefetch_related("memberships__user")

    users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        form = OrganizationForm(request.POST)

        if form.is_valid():
            org = form.save(commit=False)
            org.owner = request.user
            org.save()

            Membership.objects.create(
                user=request.user,
                organization=org,
                role="admin"
            )

            create_notification.delay(
                request.user.id,
                f"You created organization: {org.name}"
            )

            return redirect("organizations_page")
    else:
        form = OrganizationForm()

    return render(request, "organizations.html", {
        "organizations": orgs,
        "form": form,
        "users": users,
    })


@login_required
def add_member(request, org_id):

    org = get_object_or_404(Organization, id=org_id)

    is_owner = org.owner == request.user
    is_admin = Membership.objects.filter(
        user=request.user,
        organization=org,
        role="admin"
    ).exists()

    if not (is_owner or is_admin):
        return HttpResponseForbidden("You don't have permission.")

    if request.method == "POST":

        user_id = request.POST.get("user")
        role = request.POST.get("role")

        if not user_id:
            return redirect("organizations_page")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect("organizations_page")

        if not Membership.objects.filter(user=user, organization=org).exists():

            Membership.objects.create(
                user=user,
                organization=org,
                role=role
            )

            create_notification.delay(
                user.id,
                f"You were added to organization: {org.name}"
            )

    return redirect("organizations_page")


@login_required
def delete_organization(request, pk):

    org = get_object_or_404(
        Organization,
        pk=pk,
        owner=request.user
    )

    org.delete()

    return redirect("organizations_page")