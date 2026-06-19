from . import views
from django.urls import path

app_name = 'accounts_profiles'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('all_users/', views.all_users, name='all_users'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    # path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
]