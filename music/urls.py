from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from music import views

urlpatterns = [
    path("music/", views.MusicList.as_view()),
    path("music/<int:pk>/", views.MusicDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
