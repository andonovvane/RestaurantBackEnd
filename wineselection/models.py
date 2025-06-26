from django.db import models

class Wine(models.Model):
    WINE_TYPES = [
        ('red', 'Red'),
        ('white', 'White'),
        ('rose', 'Rosé'),
        ('sparkling', 'Sparkling'),
    ]

    wine_type = models.CharField(max_length=10, choices=WINE_TYPES, default='red')
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    price = models.IntegerField()
    description = models.CharField(max_length=100, blank=True)
    stock_of_wine = models.IntegerField(default=0)
    image_item = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.get_wine_type_display()})'
