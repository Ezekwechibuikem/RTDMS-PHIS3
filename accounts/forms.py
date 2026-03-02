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
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-icon-input pe-6',
            'placeholder': 'Password',
            'autocomplete': 'off'
        })
    )
