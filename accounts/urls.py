from django.urls import path
from accounts.views import EmailLoginView, MeView

app_name = 'accounts'

urlpatterns = [
    path('login/', EmailLoginView.as_view(), name='email-login'),
    path('me/', MeView.as_view()),
]
