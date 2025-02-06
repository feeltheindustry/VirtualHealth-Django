from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, roles, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            roles=roles
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, roles, password):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            roles=roles
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user  # ✅ Fix: Return user


class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]

    SPECIALIZATION_CHOICES = [
        ('cardiologist', 'Cardiologist'),
        ('neurologist', 'Neurologist'),
        ('pediatrician', 'Pediatrician'),
        ('orthopedic', 'Orthopedic'),
        ('general', 'General Practitioner'),
        ('other', 'Other')
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=200, blank=False)
    roles = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')  # ✅ Fix: Default is 'patient'
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)  # ✅ Fix: Optional
    bio = models.TextField(blank=True, null=True)
    contact_details = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'roles']

    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if self.roles != 'doctor': 
            self.specialization = None
        elif not self.specialization:
            raise ValueError("Doctors must choose a specialization.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.roles}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
