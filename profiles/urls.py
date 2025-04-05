from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views

urlpatterns = [
    path("profile/", views.ProfileList.as_view()),

    path("profile/one/", views.ProfileSingleDetail.as_view()),
    path("profile/<int:pk>", views.ProfileDetail.as_view()),

]


urlpatterns = format_suffix_patterns(urlpatterns)
