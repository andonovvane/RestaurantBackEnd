from rest_framework import serializers
from wineselection.models import Wine

class WineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ['id' ,'wine_type', 'name', 'cost', 'price', 'description', 'stock_of_wine', 'image_item']
        extra_kwargs = {
            'cost': {'write_only': True}
        }