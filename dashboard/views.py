from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.core.files.storage import default_storage
import os
from .helpers import delete_user_profile_images
import logging

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    logger.info("🔥 profile_view: Request method: %s", request.method)

    if request.method == 'POST':
        logger.info("🔥 profile_view: Form submitted here (NOT edit_profile!)")
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            logger.info("✅ Form is valid.")

            if 'image' in request.FILES:
                logger.info("🔄 Deleting old images for user: %s", request.user.id)
                delete_user_profile_images(request.user)
                messages.success(request, "Profile picture updated successfully.")

            form.save()
            messages.success(request, "Profile saved successfully.")
            return redirect('profile_view')
        else:
            logger.error("❌ Form is invalid.")
            logger.error(form.errors)
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'dashboard/profile/view_profile.html', {
        'form': form,
        'profile': profile
    })

from django.contrib import messages

logger = logging.getLogger(__name__)

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            logger.info("✅ Form is valid.")

            if 'image' in request.FILES:
                logger.info("🔄 Deleting old images...")
                logger.info(f"User ID: {request.user.id}")
                delete_user_profile_images(request.user)

            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_view')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'dashboard/profile/edit_profile.html', {'form': form})