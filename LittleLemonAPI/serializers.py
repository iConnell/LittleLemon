from rest_framework.serializers import ModelSerializer
from .models import MenuItem, Cart, Order


class MenuItemSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = MenuItem


class CartSerializer(ModelSerializer):
    class Meta:
        exclude = ['user']
        model = Cart

    
class OrderSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Order