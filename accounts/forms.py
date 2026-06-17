from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


# =========================================================
# USER REGISTRATION FORM
# =========================================================
class CustomUserCreationForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email',
            'autocomplete': 'off'
        })
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    middle_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Middle name (optional)'
        })
    )

    role = forms.ChoiceField(
        choices=[('', 'Select a role')] + list(User.ROLE_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    gender = forms.ChoiceField(
        choices=[('', 'Select gender')] + list(User.GENDER_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        }),
        help_text=password_validation.password_validators_help_text_html()
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'role',
            'image',
        )

    # -----------------------------------------------------
    # Email uniqueness validation
    # -----------------------------------------------------
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    # -----------------------------------------------------
    # Password validation
    # -----------------------------------------------------
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        password_validation.validate_password(password2, self.instance)
        return password2

    # -----------------------------------------------------
    # Save user with hashed password
    # -----------------------------------------------------
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


# =========================================================
# LOGIN FORM
# =========================================================
class CustomAuthenticationForm(AuthenticationForm):

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-icon-input',
            'placeholder': 'name@example.com',
            'autocomplete': 'off'
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-icon-input pe-6',
            'placeholder': 'Password',
            'autocomplete': 'off',
            'id': 'id_password1'
        })
    )

class ForgotPasswordForm(forms.Form):
    """Form for users to request a password reset via email."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user is associated with this email address.")
        return email

class OTPVerificationForm(forms.Form):
    """Form for users to enter the OTP sent to their email."""
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter OTP'
        })
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError("Invalid OTP format. OTP must be a 6-digit number.")
        return otp
    
class ResetPasswordForm(forms.Form):
    """Form for users to reset their password after OTP verification."""
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
             'id': 'id_password1'
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
             'id': 'id_password2'
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data