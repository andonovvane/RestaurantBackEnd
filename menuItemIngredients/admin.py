from django.contrib import admin
from .models import MenuItemIngredient

class MenuItemIngredientInline(admin.TabularInline):
    model = MenuItemIngredient
    extra = 1