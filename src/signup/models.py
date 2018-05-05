from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in, user_logged_out


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

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


