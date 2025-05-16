from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from accounts.forms import CustomUserCreationForm
from accounts.models import EmailVerificationToken, CustomUser


# Create your views here.
def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome')
            return redirect('home')
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

    messages.success(request, "Email verified successfully. You can now log in.")
    return redirect("signin")

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