from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("users.urls")),
    path("", include("artist.urls")),
    path("", include("profiles.urls")),
    path("", include(("music.urls"))),
    path("admin/", admin.site.urls),
]
