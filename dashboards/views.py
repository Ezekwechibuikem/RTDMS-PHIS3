from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboards/dashboard.html')


@login_required
def profile(request):
    display_profile = request.user
    context = {
        'display_profile': display_profile
    }
    return render(request, 'dashboards/profile.html', context)