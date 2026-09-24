from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from .forms import ProfileForm
from .models import Profile
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )

        if form.is_valid():
            form.save()

            return redirect("profile")

    else:
        form = ProfileForm(
            instance=profile,
            user=request.user
        )

    return render(request, "account/profile.html", {
        "profile_user": request.user,
        "article_count": request.user.articles.count(),
        "form": form,
    })


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "account/register.html", {
        "form": form
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "account/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")