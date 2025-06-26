# from rest_framework import  serializers
#
# from ingredients.serializers import IngredientSerializer
# from menuItems.models import MenuItem
#
# class MenuItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ['name', 'price', 'description', 'category', 'ingredients']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['ingredients'] = IngredientSerializer(instance.ingredients, many=True).data
#         return representation

from rest_framework import serializers
from menuItems.models import MenuItem
from menuItemIngredients.serializers import MenuItemIngredientCreateSerializer
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer

class MenuItemSerializer(serializers.ModelSerializer):
    ingredients = MenuItemIngredientCreateSerializer(many=True, write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'category', 'ingredients', 'image_item']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        menu_item = MenuItem.objects.create(**validated_data)
        for item_data in ingredients_data:
            ingredient_name = item_data['ingredient_name']
            quantity = item_data['quantity']
            try:
                ingredient = Ingredient.objects.get(name__iexact=ingredient_name)
                from menuItemIngredients.models import MenuItemIngredient
                MenuItemIngredient.objects.create(menu_item=menu_item, ingredient=ingredient, quantity=quantity)
            except Ingredient.DoesNotExist as e:
                raise serializers.ValidationError({"ingredients": [f"Ingredient with name '{ingredient_name}' does not exist."]})
        print("Image received:", validated_data.get("image_item"))
        return menu_item

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle ingredients update
        if ingredients_data is not None:
            from menuItemIngredients.models import MenuItemIngredient
            instance.menuitemingredient_set.all().delete()  # Remove existing ingredients

            for item_data in ingredients_data:
                ingredient_name = item_data['ingredient_name']
                quantity = item_data['quantity']
                try:
                    ingredient = Ingredient.objects.get(name__iexact=ingredient_name)
                    MenuItemIngredient.objects.create(menu_item=instance, ingredient=ingredient, quantity=quantity)
                except Ingredient.DoesNotExist:
                    raise serializers.ValidationError({"ingredients": [f"Ingredient with name '{ingredient_name}' does not exist."]})

        return instance

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['ingredients'] = IngredientSerializer(instance.ingredients, many=True).data
    #     return representation

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientSerializer(instance.ingredients, many=True).data

        # Add full image URL if image exists
        request = self.context.get('request')
        if instance.image_item:
            if hasattr(instance.image_item, 'url'):
                representation['image_item'] = request.build_absolute_uri(
                    instance.image_item.url) if request else instance.image_item.url
            else:
                representation['image_item'] = str(instance.image_item)
        return representation
