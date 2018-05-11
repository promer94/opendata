from django.contrib import admin
from .models import Profile
from app.admin import FavoriteFoodInline, FoodEntryInline
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_token', 'auth_secret', 'create_date')
    list_filter = ['user', 'create_date']
    search_fields = ['user', 'create_date']
    fieldsets = [
        (None, {'fields': ['user']})
    ]
    inlines = [FavoriteFoodInline, FoodEntryInline]


admin.site.register(Profile, ProfileAdmin)
