from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Notification
from django.contrib.auth import get_user_model
from organizations.models import Membership
from projects.models import Project

User = get_user_model()


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["recipient", "project", "message"]


@login_required
def notifications_page(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related("project").order_by("-created_at")

    if request.method == "POST":
        form = NotificationForm(request.POST)

        if form.is_valid():
            notification = form.save(commit=False)

            if notification.project:
                org = notification.project.organization

                is_admin = Membership.objects.filter(
                    user=request.user,
                    organization=org,
                    role="admin"
                ).exists()

                if is_admin:
                    notification.save()
                    return redirect("notifications_page")
            else:
                # If no project selected, just save
                notification.save()
                return redirect("notifications_page")
    else:
        form = NotificationForm()

    unread_count = notifications.filter(is_read=False).count()

    return render(request, "notifications.html", {
        "notifications": notifications,
        "form": form,
        "unread_count": unread_count,
    })


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("notifications_page")