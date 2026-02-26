from django.urls import path
from .views import RegisterView, LoginView, MeView
from .html_views import users_page, delete_user, logout_view


urlpatterns = [

    # =========================
    # API ROUTES
    # =========================
    path("register/", RegisterView.as_view(), name="api_register"),
    path("login/", LoginView.as_view(), name="api_login"),
    path("me/", MeView.as_view(), name="api_me"),

    # =========================
    # HTML USER MANAGEMENT
    # =========================
    path("page/", users_page, name="users_page"),
    path("delete/<int:pk>/", delete_user, name="delete_user"),
    path("logout/", logout_view, name="logout"),

]