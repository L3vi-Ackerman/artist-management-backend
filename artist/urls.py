from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from artist import views

urlpatterns = [
    path("artist/", views.ArtistList.as_view()),
    path("artist/<int:pk>", views.ArtistDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
