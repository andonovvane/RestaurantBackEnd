from django.db import models

# Create your models here.
class Ingredient(models.Model):
    UNIT_CHOICES=[
        ('g', 'gram'),
        ('ml', 'mililiter'),
        ('pc', 'piece'),
    ]

    name = models.CharField(max_length=150, unique=True)
    stock_quantity = models.FloatField(default=0)
    cost_per_unit = models.FloatField(default=0)
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name