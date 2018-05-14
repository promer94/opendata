import os

from django.contrib.auth.models import User
from django.db import models

from app.fatsecret import Fatsecret


class ProfileManager(models.Manager):
    def create_profile(self, user, current_weight, current_height, goal_weight):
        fs = Fatsecret(os.environ.get('API_KEY'), os.environ.get('API_SECRET'))
        session_token = fs.profile_create()
        fs = Fatsecret(os.environ.get('API_KEY'),
                       os.environ.get('API_SECRET'), session_token)
        fs.weight_update(current_weight_kg=current_weight,
                         goal_weight_kg=current_height, current_height_cm=goal_weight)
        profile = self.create(user=user,
                              auth_token=session_token[0],
                              auth_secret=session_token[1],
                              current_weight=current_weight,
                              current_height=current_height,
                              goal_weight=goal_weight
                              )
        return profile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    auth_token = models.CharField(max_length=50, null=True, blank=True)
    auth_secret = models.CharField(max_length=50, null=True, blank=True)
    current_weight = models.IntegerField(null=True, blank=True)
    current_height = models.IntegerField(null=True, blank=True)
    goal_weight = models.IntegerField(null=True, blank=True)
    objects = ProfileManager()

    class Meta:
        db_table = 'auth_profile'
        app_label = 'signup'

    def __str__(self):
        return self.user.get_username()

    def get_session_token(self):
        if self.auth_token and self.auth_secret:
            return [self.auth_token, self.auth_secret]
        else:
            return None

    def get_current_weight(self):
        return self.current_weight

    def get_current_height(self):
        return self.current_height

    def get_goal_weight(self):
        return self.goal_weight
