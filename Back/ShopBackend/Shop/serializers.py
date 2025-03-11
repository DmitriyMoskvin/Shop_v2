from rest_framework import serializers
from .models import Product, Sizes, Sections, Categories, Colors, ProductImage, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('__all__')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('__all__')


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('__all__')


class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = ('__all__')


class SizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'id']


class ProductDetaiSerializer(serializers.ModelSerializer):
    section = SectionsSerializer()
    category = CategoriesSerializer()
    size = SizesSerializer(many=True)
    colors = ColorSerializer(many=True)
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ('__all__')


class ProductListSerializer(serializers.ModelSerializer):
    section = SectionsSerializer()
    category = CategoriesSerializer()
    size = SizesSerializer(many=True)
    colors = ColorSerializer(many=True)
    class Meta:
        model = Product
        fields = ('__all__')


class FiltersListSerializer(serializers.Serializer):
    sizes = SizesSerializer(many=True)
    colors = ColorSerializer(many=True)
    category = CategoriesSerializer(many=True)
