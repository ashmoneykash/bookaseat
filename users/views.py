from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('movie_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    # Auto-create profile if it doesn't exist
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        # ── Update basic info ──
        if action == 'update_info':
            user = request.user
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name  = request.POST.get('last_name', '').strip()
            user.email      = request.POST.get('email', '').strip()
            user.save()

            user_profile.phone   = request.POST.get('phone', '').strip()
            user_profile.address = request.POST.get('address', '').strip()

            if 'profile_pic' in request.FILES:
                user_profile.profile_pic = request.FILES['profile_pic']

            user_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

        # ── Change password ──
        elif action == 'change_password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
            else:
                for error in form.errors.values():
                    messages.error(request, error.as_text().replace('* ', ''))
            return redirect('profile')

    return render(request, 'users/profile.html', {
        'user_profile': user_profile,
    })