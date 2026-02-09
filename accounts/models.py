from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            **extra_fields
            )

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('DepartmentHead', 'Department Head'),
        ('UnitHead', 'Unit Head'),
        ('SUPERVISOR', 'Supervisor'),
        ('STAFF', 'Staff'),
    )
    
    TEAM_CHOICES = (
        ('TEAM1', 'Team 1'),
        ('TEAM2', 'Team 2'),
        ('TEAM3', 'Team 3'),
        ('TEAM4', 'Team 4'),
        ('TEAM5', 'Team 5'),
        ('TEAM6', 'Team 6'),
        ('TEAM7', 'Team 7'),
        ('TEAM8', 'Team 8'),
        ('TEAM9', 'Team 9'),
        ('TEAM10', 'Team 10'),
    )
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}, email -- {self.email}, Team -- {self.get_team_display()}"
    
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    
    def is_hr(self):
        return self.role == 'HR'
    
    def is_it(self):
        return self.role == 'IT'
    
    def is_department_head(self):
        return self.role == 'DepartmentHead'
    
    def is_unit_head(self):
        return self.role == 'UnitHead'
    
    def is_supervisor(self):
        return self.role == 'SUPERVISOR'
    
    def is_staff_member(self):
        return self.role == 'STAFF'
