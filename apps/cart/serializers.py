
from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity', 'added_at']

    def get_item(self, obj):
        item = obj.item
        # Customize based on item type; add more fields as needed
        return {
            "id": item.id,
            "name": str(item),
            "type": obj.content_type.model  # E.g., 'tourpackage', 'hotel', 'guide'
        }

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']