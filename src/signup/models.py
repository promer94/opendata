import os
from django.db import models
from django.contrib.auth.models import User
from app.fatsecret import Fatsecret


class ProfileManager(models.Manager):
    def create_profile(self, user):
        fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'))
        session_token = fs.profile_create()
        profile = self.create(user=user, auth_token=session_token[0], auth_secret=session_token[1])
        return profile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=50, null=True, blank=True)
    auth_secret = models.CharField(max_length=50, null=True, blank=True)
    objects = ProfileManager()

    class Meta:
        db_table = 'auth_profile'
        app_label = 'signup'

    def __str__(self):
        return self.user.username

    def get_picture(self):
        no_picture = 'https://lh3.googleusercontent.com/-EZnfGPvftkI/AAAAAAAAAAI/AAAAAAAAA5I/in5JbhZ3bp8/s120-p-rw-no/photo.jpg'
        return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except Exception:
            return self.user.username

    def get_session_token(self):
        if self.auth_token and self.auth_secret:
            return [self.auth_token, self.auth_secret]
        else:
            return None


