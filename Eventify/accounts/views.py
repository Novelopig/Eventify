from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Q

# from django.core.files.storage import default_storage
from django.contrib import messages

# from events.models import Event
from django.contrib.auth.models import User
from accounts.models import User


def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        profile_picture = request.FILES.get("profile_picture")
        bio = request.POST.get("bio", "")
        security_question = request.POST.get("security_question", "").strip()
        security_answer = request.POST.get("security_answer", "").strip().lower()

        # Check required fields
        if not username or not email or not password1 or not password2:
            return render(
                request, "accounts/signup.html", {"error": "All fields are required."}
            )

        # Check if username or email is already taken
        if User.objects.filter(username=username).exists():
            return render(
                request, "accounts/signup.html", {"error": "Username already in use."}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request, "accounts/signup.html", {"error": "Email already registered."}
            )

        # Check if passwords match
        if password1 != password2:
            return render(
                request, "accounts/signup.html", {"error": "Passwords do not match."}
            )

        try:
            user = User(
                username=username,
                email=email,
                profile_picture=profile_picture,
                bio=bio,
                security_question=security_question,
                security_answer=security_answer,
            )
            user.set_password(password1)
            user.save()

            authenticated_user = authenticate(
                request, username=username, password=password1
            )
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("homepage")
            else:
                return render(
                    request,
                    "accounts/login.html",
                    {"error": "Authentication failed after signup. Try logging in."},
                )

        except ValidationError as e:
            return render(request, "accounts/signup.html", {"error": e.messages[0]})

    return render(request, "accounts/signup.html")


def user_login(request):
    if request.method == "POST":
        login_input = request.POST.get("username")
        password = request.POST.get("password")

        print(
            f"🔍 DEBUG: Trying to authenticate user '{login_input}' with password '{password}'"
        )

        user = User.objects.filter(
            Q(username=login_input) | Q(email=login_input)
        ).first()

        if user:
            print(f"🔍 DEBUG: Found user '{user.username}', checking password...")

            authenticated_user = authenticate(
                request, username=user.username, password=password
            )

            if authenticated_user:
                print(f"✅ DEBUG: Authentication successful for user '{user.username}'")
                login(request, authenticated_user)
                return redirect("homepage")
            else:
                print(
                    f"❌ DEBUG: Authentication failed for user '{login_input}'. Password may be incorrect."
                )
                return render(
                    request,
                    "accounts/login.html",
                    {"error": "Invalid username or password."},
                )
        else:
            print(f"❌ DEBUG: No user found with username/email '{login_input}'")
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid username or password."},
            )

    return render(request, "accounts/login.html")


def user_logout(request):
    previous_page = request.META.get("HTTP_REFERER", "/")

    logout(request)

    return redirect(previous_page)


def password_reset_request(request):
    if request.method == "POST":
        login_input = request.POST.get("login_input").strip()

        if not login_input:
            return render(
                request,
                "accounts/password_reset_request.html",
                {"error": "Please enter a username or email."},
            )

        user = User.objects.filter(
            Q(username=login_input) | Q(email=login_input)
        ).first()

        if user:
            if user.security_question:
                return redirect(
                    "accounts:password_reset_verify", username=user.username
                )
            else:
                return render(
                    request,
                    "accounts/password_reset_request.html",
                    {"error": "Security question is not set for this account."},
                )
        else:
            return render(
                request,
                "accounts/password_reset_request.html",
                {"error": "User not found."},
            )

    return render(request, "accounts/password_reset_request.html")


def password_reset_verify(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        security_answer = request.POST.get("security_answer", "").strip().lower()

        if (
            user.security_answer
            and user.security_answer.lower().strip() == security_answer
        ):
            return render(
                request,
                "accounts/password_reset_confirm.html",
                {
                    "username": user.username,
                    "correct_answer": True,
                },
            )
        else:
            return render(
                request,
                "accounts/password_reset_question.html",
                {"user": user, "error": "Incorrect security answer. Please try again."},
            )

    return render(request, "accounts/password_reset_question.html", {"user": user})


def password_reset_confirm(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        new_password = request.POST.get("new_password").strip()
        confirm_password = request.POST.get("confirm_password").strip()

        if new_password != confirm_password:
            return render(
                request,
                "accounts/password_reset_confirm.html",
                {
                    "error": "Passwords do not match.",
                    "username": username,
                    "correct_answer": True,
                },
            )

        user.set_password(new_password)
        user.save()

        messages.success(
            request,
            "Your password has been reset successfully. Please log in with your new password.",
        )

        return redirect("accounts:login")

    return render(
        request,
        "accounts/password_reset_confirm.html",
        {"username": username, "correct_answer": True},
    )


@login_required
def password_update(request):
    user = request.user

    if request.method == "POST":
        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not user.check_password(current_password):
            return render(
                request,
                "accounts/password_update.html",
                {"error": "Current password is incorrect."},
            )

        if new_password != confirm_password:
            return render(
                request,
                "accounts/password_update.html",
                {"error": "New passwords do not match."},
            )

        if len(new_password) < 8:
            return render(
                request,
                "accounts/password_update.html",
                {"error": "Password must be at least 8 characters long."},
            )

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been updated successfully!")

        return redirect("homepage")

    return render(request, "accounts/password_update.html")


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST.get("email")
        user.bio = request.POST.get("bio")
        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]
        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect("accounts:dashboard")

    return render(request, "accounts/edit_profile.html")
