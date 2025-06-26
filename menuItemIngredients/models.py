from django.db import models

class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey('menuItems.MenuItem', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('ingredients.Ingredient', on_delete=models.CASCADE)
    quantity = models.FloatField()

    def unit(self):
        return self.ingredient.unit

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.menu_item.name}"
