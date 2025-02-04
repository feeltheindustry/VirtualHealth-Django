from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.
class CustomUserManager(UserManager):
    def _create_users(self, email, password, **extra_fields):
        if not email:
            raise ValueError("No valid email address provided")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
    def create_user(self, email = None,password = None, **extra_fields):
        extra_fields.setdefault('is_doctor', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_users(email, password, **extra_fields)
    
    def create_admin(self, email = None,password = None, **extra_fields):
        extra_fields.setdefault('is_doctor', False)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_users(email, password, **extra_fields)
    
    def create_doctor(self, email = None,password = None, **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        extra_fields.setdefault('is_admin', False) 
        extra_fields.setdefault('is_staff', True)
        return self._create_users(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length = 255, blank = True, default = "")
    email = models.EmailField(blank = True, default="", unique = True)

    is_active = models.BooleanField(default = True)
    is_doctor = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)

    date_joined  = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(blank = True, null = True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0] 
        