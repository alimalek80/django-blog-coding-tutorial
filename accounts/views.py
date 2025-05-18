from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from accounts.forms import CustomUserCreationForm, PasswordResetRequestForm, PasswordResetConfirmForm
from accounts.models import EmailVerificationToken, CustomUser, PasswordResetToken
from dashboard.models import Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
import json
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.get(email=email)

            # Delete any old tokens
            PasswordResetToken.objects.filter(user=user).delete()

            # Generate new token
            token_obj = PasswordResetToken.create_token(user)

            # Build reset URL
            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", args=[token_obj.token])
            )

            # Send email
            subject = "Password Reset Request"
            html_message = render_to_string("accounts/password_reset_email.html", {
                "reset_url": reset_url,
                "user": user,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

            return redirect("password_reset_done")

    else:
        form = PasswordResetRequestForm()

    return render(request, "accounts/password_reset_form.html", {"form": form})

def password_reset_confirm(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)

    if not token_obj.is_valid():
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect("password_reset_request")

    if request.method == "POST":
        form = PasswordResetConfirmForm(request.POST, user=token_obj.user)
        if form.is_valid():
            form.save()
            token_obj.is_used = True
            token_obj.save()
            messages.success(request, "Your password has been reset successfully. Please log in.")
            return redirect("signin")
    else:
        form = PasswordResetConfirmForm(user=token_obj.user)

    return render(request, "accounts/password_reset_confirm.html", {
        "form": form,
        "token": token,
    })

def password_reset_done(request):
    return render(request, "accounts/password_reset_done.html")

def password_reset_complete(request):
    return render(request, "accounts/password_reset_complete.html")

@csrf_exempt
@login_required
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            user = request.user

            # Check if the current password is correct
            if not check_password(current_password, user.password):
                return JsonResponse({'success': False, 'message': 'Current password is incorrect.'}, status=400)

            # Set and save the new password
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            # Check if profile exists and redirect accordingly
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)

            # Option1: Check if profile is incomplete
            if not profile.city and not profile.country:
                messages.info(request, "Please complete your profile.")
                return redirect("edit_profile")
            else:
                return redirect("dashboard_home")

        else:
            messages.warning(request, "Wrong information")
            return redirect('signin')
    else:
        return render(request, 'accounts/login.html', {})


def logout_view(request):
    logout(request)
    messages.success(request, "Your logged out.")
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = EmailVerificationToken.create_token_for_user(user)

            confirmation_url = request.build_absolute_uri(
                reverse("verify_email", args=[token.token])
            )

            send_mail(
                subject="Confirm Your Email",
                message=f"Please click the link below to confirm your Email:\n\n{confirmation_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            messages.success(request, "Registration successful. Please Check Your Email to verify your account.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def verify_email(request, token):
    email_token = get_object_or_404(EmailVerificationToken, token=token)
    user = email_token.user

    if not email_token.is_valid():
        if not user.email_verified:
            return render(request, "accounts/token_expired.html", {"user": user})
        messages.error(request, "The verification link has expired.")
        return redirect("register")

    user.is_active = True
    user.email_verified = True
    user.save()

    # Delete the token after verification
    email_token.delete()

    messages.success(request, "Email verified successfully. Welcome to your dashboard.")
    login(request, user)
    return redirect("dashboard_home")

def resend_verification_email(request):
    user_id = request.POST.get("user_id")
    user = get_object_or_404(CustomUser, id=user_id)

    # Delete the old token
    EmailVerificationToken.objects.filter(user=user).delete()

    token = EmailVerificationToken.create_token_for_user(user)
    confirmation_url = request.build_absolute_uri(
        reverse("verify_email", args=[token.token])
    )

    send_mail(
        subject="Confirm Your Email - Resent",
        message=f"Please click the new link to confirm your Email:\n\n{confirmation_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    messages.success(request, "A new verification link has been sent to your email.")
    return redirect("signin")

def home_view(request):
    return render(request, "accounts/home.html", {})