from django.db import models, transaction
from django.conf import settings

from menuItems.models import MenuItem
from wineselection.models import Wine
from menuItemIngredients.models import MenuItemIngredient


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders_created"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_orders"
    )

    table_id = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_id} ({self.status})"

    @transaction.atomic
    def complete_order(self):
        if self.status == "completed":
            return

        for item in self.items.all():
            if item.item_type == "menu_item":
                menu_item = MenuItem.objects.get(id=item.item_id)
                requirements = MenuItemIngredient.objects.filter(menu_item=menu_item)

                for req in requirements:
                    total_needed = req.quantity * item.quantity
                    ingredient = req.ingredient

                    if ingredient.stock_quantity < total_needed:
                        raise ValueError(f"Not enough {ingredient.name} in stock.")

                    ingredient.stock_quantity -= total_needed
                    ingredient.save()

            elif item.item_type == "wine":
                wine = Wine.objects.get(id=item.item_id)

                if wine.stock_of_wine < item.quantity:
                    raise ValueError(f"Not enough {wine.name} in stock.")

                wine.stock_of_wine -= item.quantity
                wine.save()

        self.status = "completed"
        self.save()


class OrderItem(models.Model):
    ITEM_TYPES = [
        ("menu_item", "Menu Item"),
        ("wine", "Wine"),
        ("soft_drink", "Soft Drink"),
        ("dessert", "Dessert"),
        ("beverage", "Beverage"),
    ]

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    item_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # ← new field

    def __str__(self):
        return f"{self.quantity} x {self.item_type} #{self.item_id} (Order {self.order.id})"