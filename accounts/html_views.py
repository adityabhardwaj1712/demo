from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import logout


User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_active"]


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def users_page(request):
    users = User.objects.all()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users_page")
    else:
        form = UserForm()

    return render(request, "users.html", {
        "users": users,
        "form": form,
    })


@login_required
@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect("users_page")

@login_required
def logout_view(request):
    logout(request)
    return redirect("/api/accounts/login/")