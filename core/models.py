from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.PositiveBigIntegerField()
    dob = models.DateField()
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Artist(models.Model):
    GENDER = (("M", "Male"), ("F", "Female"), ("O", "Other"))
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=1, default="M", choices=GENDER)
    first_release_year = models.DateField()
    no_of_albumns_released = models.IntegerField()
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
    artist_id = models.ManyToManyField(Artist, through="ArtistMusic")
    title = models.CharField(max_length=255)
    albumn_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=7)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ArtistMusic(models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    music_id = models.ForeignKey(Music, on_delete=models.CASCADE)
