from django.db import models
from ingredients.models import Ingredient

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('main_course', 'Main Course'),
        ('desserts', 'Desserts'),
    ]

    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_item = models.URLField(blank=True, null=True)
    ingredients = models.ManyToManyField("ingredients.Ingredient", through="menuItemIngredients.MenuItemIngredient")

    def __str__(self):
        return self.name
