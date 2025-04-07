from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import choices, timezone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ("SUPER_ADMIN", "super admin"),
        ("ARTIST", "Artist"),
        ("ARTIST_MANAGER", "Artist Manager"),
    )
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLES, default="ARTIST")
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):
        pass

    def __str__(self) -> str:
        return str(self.email)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=10,null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(default=timezone.now,null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Artist(models.Model):
    GENDER = (("M", "Male"), ("F", "Female"), ("O", "Other"))

    manager = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255,null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=1, default="M", choices=GENDER, null=True)
    address = models.CharField(max_length=255, null=True)
    first_release_year = models.CharField(null=True)
    no_of_albumns_released = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Music(models.Model):
    GENRE = (
        ("rnb", "RNB"),
        ("c", "country"),
        ("cl", "classic"),
        ("r", "rock"),
        ("j", "jazz"),
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE    )
    
    title = models.CharField(max_length=255,null=True)
    album_name = models.CharField(max_length=255,null=True)
    genre = models.CharField(max_length=7,null=True)
    created_at = models.DateTimeField(default=timezone.now,null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
