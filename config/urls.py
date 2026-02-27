from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from projects.html_views import dashboard
from projects.html_views import tasks_page
from accounts.html_views import users_page

urlpatterns = [

    path("admin/", admin.site.urls),

    # AUTH
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

    # DASHBOARD
    path("dashboard/", dashboard, name="dashboard"),

    # MAIN APPS
    path("projects/", include("projects.urls")),
    path("organizations/", include("organizations.urls")),
    path("notifications/", include("notifications.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/accounts/", include("accounts.api_urls")),

    # 🔥 SHORTCUT ROUTES (So your old UI links work)
    path("tasks/page/", tasks_page),
    path("users/page/", users_page),
]