from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from accounts_profiles.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'staffs/profile.html', {'profile': profile})

@login_required
def all_users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'staffs/all_users.html', context)

@login_required
def user_detail(request, user_id):
    selected_user = get_object_or_404(User, id=user_id)
    # profile, _ = UserProfile.objects.get_or_create(user=selected_user)
    context = {
        'user': selected_user,
        # 'profile': profile,
    }
    return render(request, 'staffs/user_detail.html', context)