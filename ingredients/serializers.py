from rest_framework import serializers
from ingredients.models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name', 'stock_quantity', 'cost_per_unit', 'unit']
        extra_kwargs = {
            'cost_per_unit': {'write_only': True}
        }
