from . import views
from django.urls import path

app_name = 'accounts_profiles'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
]