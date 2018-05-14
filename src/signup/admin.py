from django.contrib import admin

from app.admin import FavoriteFoodInline, FoodEntryInline

from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'current_weight',
                    'current_height',
                    'goal_weight',
                    'auth_token',
                    'auth_secret',
                    'create_date')
    list_filter = ['user', 'create_date']
    search_fields = ['user', 'create_date']
    fieldsets = [
        (None, {'fields': ['user']}),
        ('Health data', {'fields': [
         'current_weight', 'current_height', 'goal_weight']})
    ]
    inlines = [FavoriteFoodInline, FoodEntryInline]


admin.site.register(Profile, ProfileAdmin)
