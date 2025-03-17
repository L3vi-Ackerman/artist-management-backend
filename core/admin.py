from django.contrib import admin
from .models import CustomUser, Profile, Music, Artist

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Music)
admin.site.register(Artist)
