import django_filters
from .models import Product, Item

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price_per_unit", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price_per_unit", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'size', 'colors', 'min_price', 'max_price']


class ProductBySectionFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name='category__id', lookup_expr='in', distinct=True)
    size = NumberInFilter(field_name='size__id', lookup_expr='in', distinct=True)
    colors = NumberInFilter(field_name='colors__id', lookup_expr='in', distinct=True)
    price_per_unit = django_filters.RangeFilter()


    class Meta:
        model = Product
        fields = ['category', 'size', 'colors', 'price_per_unit']


class ItemByFiltersFilter(django_filters.FilterSet):
    color = NumberInFilter(field_name='color', lookup_expr='in', distinct=True)
    size = NumberInFilter(field_name='size', lookup_expr='in', distinct=True)
