from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["message"]


@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(user=request.user)

    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return redirect("notifications_page")
    else:
        form = NotificationForm()

    return render(request, "notifications.html", {
        "notifications": notifications,
        "form": form,
    })


# ✅ THIS FUNCTION WAS MISSING
@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect("notifications_page")