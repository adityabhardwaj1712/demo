from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Notification
from organizations.models import Membership


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["recipient", "project", "message"]


@login_required
def notifications_page(request):

    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related("project")
    )

    if request.method == "POST":
        form = NotificationForm(request.POST)

        if form.is_valid():
            notification = form.save(commit=False)

            if notification.project:
                org = notification.project.organization

                is_admin = Membership.objects.filter(
                    user=request.user,
                    organization=org,
                    role="admin"   # FIXED lowercase
                ).exists()

                if not is_admin:
                    return redirect("notifications_page")

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