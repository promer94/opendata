from django.contrib import admin
from .models import FavoriteFood, FoodEntry


# Register your models here.
class FavoriteFoodInline(admin.TabularInline):
    model = FavoriteFood
    extra = 3


class FoodEntryInline(admin.TabularInline):
    model = FoodEntry
    extra = 3


class FavoriteFoodAdmin(admin.ModelAdmin):
    list_display = ('profile', 'food_id', 'add_date')
    list_filter = ['profile', 'food_id', 'add_date']
    search_fields = ['profile', 'food_id', 'add_date']
    fieldsets = [
        (None, {'fields': ['profile']})
    ]


class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ('profile', 'food_entry_id', 'entry_create_date')
    list_filter = ['profile', 'food_entry_id', 'entry_create_date']
    search_fields = ['profile', 'food_entry_id', 'entry_create_date']
    fieldsets = [
        (None, {'fields': ['profile']})
    ]


admin.site.register(FavoriteFood, FavoriteFoodAdmin)
admin.site.register(FoodEntry, FoodEntryAdmin)
