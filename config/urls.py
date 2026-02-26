from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from projects.html_views import dashboard

urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            redirect_authenticated_user=True
        ),
        name="login",
    ),

    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),

    path("dashboard/", dashboard, name="dashboard"),

    # ONLY HERE
    path("projects/", include("projects.urls")),
    path("organizations/", include("organizations.urls")),
    path("notifications/", include("notifications.urls")),

    path("api/accounts/", include("accounts.urls")),
]