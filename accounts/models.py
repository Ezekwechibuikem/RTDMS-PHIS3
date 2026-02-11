from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DEPT_HEAD', 'Department Head'),
        ('UNIT_HEAD', 'Unit Head'),
        ('SUPERVISOR', 'Supervisor'),
        ('STAFF', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    def is_department_head(self):
        return self.role == 'DEPT_HEAD'

    def is_unit_head(self):
        return self.role == 'UNIT_HEAD'

    def is_supervisor(self):
        return self.role == 'SUPERVISOR'

    def is_staff_member(self):
        return self.role == 'STAFF'
