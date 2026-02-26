from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name"]


@login_required
def organizations_page(request):
    orgs = Organization.objects.filter(owner=request.user)

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.owner = request.user
            org.save()
            return redirect("organizations_page")
    else:
        form = OrganizationForm()

    return render(request, "organizations.html", {
        "organizations": orgs,
        "form": form,
    })


@login_required
def delete_organization(request, pk):
    org = get_object_or_404(Organization, pk=pk, owner=request.user)
    org.delete()
    return redirect("organizations_page")