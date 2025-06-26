from rest_framework import serializers
from menuItemIngredients.models import MenuItemIngredient
from ingredients.serializers import IngredientSerializer
from ingredients.models import Ingredient

# Used for read/display
class MenuItemIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = MenuItemIngredient
        fields = ['menu_item', 'ingredient', 'quantity']

# Used for creation
class MenuItemIngredientCreateSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField(write_only=True)
    quantity = serializers.FloatField()
    ingredient = IngredientSerializer(read_only=True)  # Display after creation

    def validate_ingredient_name(self, value):
        if not Ingredient.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(f"Ingredient with name '{value}' does not exist.")
        return value

    def create(self, validated_data):
        raise NotImplementedError("Creation should be handled in the parent serializer.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Update should be handled in the parent serializer.")
