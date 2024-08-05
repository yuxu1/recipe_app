from django.urls import path
from .views import ProfileView, signup

app_name = "users"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("signup/", signup, name="signup")
]
