from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AppUser(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text="this will be visible to others")
    bio = models.TextField(max_length=1000, null=True, blank=True, default="")
    pic = models.ImageField(upload_to="users", default="blank-profile-picture.png")

    def __str__(self):
        return str(self.name)
