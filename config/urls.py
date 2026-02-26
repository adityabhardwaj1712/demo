# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Add only this import for dashboard
from projects.html_views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login / Logout
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

    # Dashboard – working route
    path("dashboard/", dashboard, name="dashboard"),

    # Keep commented until ready
    # path("projects/", project_views.project_list, name="project_list"),
    # path("projects/<int:id>/", project_views.project_detail, name="project_detail"),

    path("api/accounts/", include("accounts.urls")),
    path("api/orgs/", include("organizations.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/notifications/", include("notifications.urls")),
]