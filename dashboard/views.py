from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'dashboard/profile/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'dashboard/profile/edit_profile.html', {'form': form})
