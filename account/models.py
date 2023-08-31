import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, username=None):
        if not email:
            raise ValueError("User must have amil address")

        user = self.model(
            email=self.normalize_email(email),
            username=str(uuid.uuid4())[:10],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None, username=None):
        user = self.create_user(
            email=email,
            last_name=last_name,
            first_name=first_name,
            password=password,
            username=str(uuid.uuid4())[6]
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save()
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, unique=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures',
                                        blank=True, null=True, default='users/profile_pictures/def_prof.png')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def get_email(self):
        return self.user.email

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
