from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    path("user/", views.UserList.as_view()),
    path("user/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("login/", views.LoginView.as_view()),
    path("signup/", views.SignupView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
