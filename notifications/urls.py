from django.urls import path
from .html_views import notifications_page, mark_notification_read
from .views import NotificationListView, MarkAsReadView

urlpatterns = [

    # HTML
    path("page/", notifications_page, name="notifications_page"),
    path("read/<int:pk>/", mark_notification_read, name="mark_notification_read"),

    # API
    path("api/", NotificationListView.as_view()),
    path("api/<int:pk>/read/", MarkAsReadView.as_view()),
]