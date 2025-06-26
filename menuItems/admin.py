from django.contrib import admin

from menuItems.models import MenuItem
from menuItemIngredients.models import MenuItemIngredient
from menuItemIngredients.admin import MenuItemIngredientInline

# class MenuItemIngredientInline(admin.TabularInline):
#     model = MenuItemIngredient
#     extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    inlines = [MenuItemIngredientInline]  # Attach inline form

admin.site.register(MenuItem, MenuItemAdmin)  # ✅ Only registering MenuItem here