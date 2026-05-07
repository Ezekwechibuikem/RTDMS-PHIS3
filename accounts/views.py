from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

from .models import *
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ForgotPasswordForm, ResetPasswordForm, OTPVerificationForm
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

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboards:dashboard')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                PasswordResetOTP.objects.filter(user=user, is_used=False).delete()
                otp = PasswordResetOTP.generate_otp()

                PasswordResetOTP.objects.create(user=user, otp=otp) 

                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                request.session['reset_email'] = user.email
                messages.success(request, "An OTP has been sent to your email address.")
                return redirect('accounts:verify_otp')
            
            except CustomUser.DoesNotExist:
                messages.error(request, "No user is associated with this email address.")
                return render(request, 'accounts/forgot_password.html', {'form': form})
            
        else:
            form = ForgotPasswordForm()
            return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, "No email found in session. Please start the password reset process again.")
        return redirect('accounts:forgot_password')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                user = CustomUser.objects.get(email=email)
                otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).latest('created_at')

                if otp_obj and otp_obj.created_at >= timezone.now() - timedelta(minutes=10):
                    otp_obj.is_used = True
                    otp_obj.save()
                    request.session['otp_verified'] = True                                                 
                    return redirect('accounts:reset_password')
                else:
                    messages.error(request, "Invalid or expired OTP. Please try again.")
                    return render(request, 'accounts/verify_otp.html', {'form': form})
            
            except PasswordResetOTP.DoesNotExist:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('accounts:forgot_password')
            
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})

def reset_password(request):
    email = request.session.get('reset_email')
    verified = request.session.get('otp_verified', False)
    if not email or not verified:
        messages.error(request, "Unauthorized access. Please start the password reset process again.")
        return redirect('accounts:forgot_password')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(password)
                user.save()

                request.session.flush()

                messages.success(request, "Your password has been reset successfully. Please login.")
                request.session.pop('reset_email', None)
                request.session.pop('otp_verified', None)
                return redirect('accounts:login')
            
            except CustomUser.DoesNotExist:
                messages.error(request, "No user is associated with this email address.")
                return redirect('accounts:forgot_password')
            
        else:
            form = ResetPasswordForm()
            return render(request, 'accounts/reset_password.html', {'form': form})