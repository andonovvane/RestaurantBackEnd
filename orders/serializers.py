from rest_framework import serializers
from .models import Order, OrderItem
from menuItems.models import MenuItem
from wineselection.models import Wine


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "item_type", "item_id", "quantity", "price_at_order", "item_name"]
        read_only_fields = ["price_at_order"]

    def get_item_name(self, obj):
        if obj.item_type == "menu_item":
            try:
                from menuItems.models import MenuItem
                item = MenuItem.objects.get(id=obj.item_id)
                return item.name
            except MenuItem.DoesNotExist:
                return f"Unknown Menu Item #{obj.item_id}"
        elif obj.item_type == "wine":
            try:
                from wineselection.models import Wine
                wine = Wine.objects.get(id=obj.item_id)
                return wine.name
            except Wine.DoesNotExist:
                return f"Unknown Wine #{obj.item_id}"
        return "Unknown Item"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "table_id", "status", "created_at", "created_by", "client", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user

        if user.role == "kitcher":
            raise serializers.ValidationError("Kitchers cannot create orders.")

        if user.role == "client":
            validated_data["table_id"] = user.table_id
            validated_data["client"] = user
        elif user.role == "waiter":
            if "table_id" not in validated_data:
                raise serializers.ValidationError({"table_id": "Waiter must provide a table_id"})
            validated_data["created_by"] = user

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            price = self._get_item_price(
                item_data["item_type"],
                item_data["item_id"]
            )
            OrderItem.objects.create(
                order=order,
                price_at_order=price,
                **item_data
            )

        return order

    def _get_item_price(self, item_type, item_id):
        """Fetch current price from the correct model"""
        try:
            if item_type == "menu_item":
                return MenuItem.objects.get(id=item_id).price
            elif item_type == "wine":
                return Wine.objects.get(id=item_id).price
            else:
                return 0
        except (MenuItem.DoesNotExist, Wine.DoesNotExist):
            raise serializers.ValidationError(
                f"{item_type} with id {item_id} does not exist."
            )