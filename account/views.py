from django.contrib import messages
from django.shortcuts import render, redirect

from account.forms import AdminSignupForm


def admin_signup(request):
    if request.method == "POST":
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully!, Kindly ask admin to give you login access for RLS"
            )
            return redirect("/admin/")
    else:
        form = AdminSignupForm()
    return render(request, "signup.html", {"form": form})
