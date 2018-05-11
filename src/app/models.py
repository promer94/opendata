from django.db import models
from signup.models import Profile


class FavoriteFood(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food_id = models.CharField(max_length=50, null=True, blank=True)
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.food_id


class FoodEntry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food_entry_id = models.CharField(max_length=50, null=True, blank=True)
    entry_create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.food_entry_id
