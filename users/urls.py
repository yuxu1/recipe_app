from django.urls import path, re_path
from .views import ProfileView, signup
from django.conf import settings
from django.views.static import serve

app_name = "users"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("signup/", signup, name="signup"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
