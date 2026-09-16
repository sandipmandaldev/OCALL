from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            if hasattr(user, "profile"):
                user.profile.is_online = True
                user.profile.save(update_fields=["is_online"])
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")
def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect("dashboard")
    return render(request, "register.html")
@login_required
def dashboard(request):
    users = User.objects.exclude(id=request.user.id).select_related("profile")
    return render(
        request,
        "dashboard.html",
        {
            "users": users,
        }
    )
def logout_view(request):
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        request.user.profile.is_online = False
        request.user.profile.save(update_fields=["is_online"])
    logout(request)
    return redirect("home")
@login_required
def call(request):
    target_user_id = request.GET.get("user")
    call_type = request.GET.get("type", "video")
    return render(request, "call.html", {
        "target_user_id": target_user_id,
        "call_type": call_type,
    })