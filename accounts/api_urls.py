from django.urls import path
from .views import RegisterView, LoginView, MeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="api_register"),
    path("login/", LoginView.as_view(), name="api_login"),
    path("me/", MeView.as_view(), name="api_me"),
]