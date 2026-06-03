import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class AbstractBaseModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            table_name = self.__class__.__name__.lower()
            self.id = f"{table_name}-{str(uuid.uuid4())}"
        super().save(*args, **kwargs)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self.create_user(email, password, **extra_fields)


class Librarian(AbstractUser, AbstractBaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
from django.conf import settings

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_FAILED',  'Login Failed'),
        ('LOGOUT',        'Logout'),
        ('CREATE',        'Create'),
        ('UPDATE',        'Update'),
        ('DELETE',        'Delete'),
        ('ACCESS_DENIED', 'Access Denied'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='audit_logs'
    )
    action      = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} | {self.action} | {self.user}"
