from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            if user.role == 'ADMIN':
                user.is_staff = True
                user.save()

            messages.success(request, "Registration successful. Please login.")
            return redirect('accounts:login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

from accounts_profiles.models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboards:dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.apply_increment()

            next_url = request.POST.get('next') or request.GET.get('next') or 'dashboards:dashboard'
            return redirect(next_url)
        messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')