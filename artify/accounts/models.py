from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from artify.accounts.managers import ArtifyUserManager


class ArtifyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    USERNAME_FIELD = 'email'

    objects = ArtifyUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
    )
    profile_image = models.ImageField(
        upload_to='profiles',
        blank=True,
    )
    location = models.CharField(
        max_length=30,
        blank=True,
    )
    user = models.OneToOneField(
        ArtifyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    is_complete = models.BooleanField(
        default=False,
    )


from .signals import *