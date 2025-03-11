from rest_framework import serializers
from .models import Customer, Order, Products
from Shop.serializers import ItemSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('total_price')


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('__all__')


class OrdersApiSerializer(serializers.Serializer):
    items = ItemSerializer(many=True)
    customer = CustomerSerializer()
    total_price = OrderSerializer()
