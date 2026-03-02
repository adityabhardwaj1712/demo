from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model, logout
from django import forms

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_staff", "is_active"]


def is_admin(user):
    return user.is_superuser


# =========================
# LIST USERS
# =========================
@login_required
@user_passes_test(is_admin)
def users_page(request):
    users = User.objects.all()
    return render(request, "users.html", {
        "users": users,
    })


# =========================
# CREATE USER (NEW PAGE)
# =========================
@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                is_staff=data["is_staff"],
                is_active=data["is_active"],
            )
            return redirect("users_page")
    else:
        form = UserForm()

    return render(request, "create_user.html", {
        "form": form,
    })


# =========================
# DELETE USER
# =========================
@login_required
@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect("users_page")


# =========================
# LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")