from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts_profiles.models import UserProfile

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'staffs/profile.html', {'profile': profile})

