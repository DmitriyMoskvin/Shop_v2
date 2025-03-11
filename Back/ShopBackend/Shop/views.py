from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Sections, Sizes, Colors, Categories, Item
from .serializers import ProductListSerializer, SectionsSerializer, FiltersListSerializer, SizesSerializer, ColorSerializer, CategoriesSerializer, ProductDetaiSerializer, ItemSerializer
from .filters import ProductFilter, ProductBySectionFilter, ItemByFiltersFilter




class ProductListAPI(generics.ListAPIView):
    '''Главная страница. Список всех товаров'''
    serializer_class = ProductListSerializer


    def get_queryset(self, **kwargs):
        queryset = Product.objects.all()
        queryset = queryset.select_related('section')
        queryset = queryset.select_related('category')
        queryset = queryset.prefetch_related('size')
        queryset = queryset.prefetch_related('colors')
        queryset = queryset.filter(isPublished=True, section__isPublished=True)

        return queryset


class ProductDetailAPI(generics.RetrieveAPIView):
    '''Определенный товар'''
    queryset = Product.objects.all()
    serializer_class = ProductDetaiSerializer

    def get_queryset(self, **kwargs):
        queryset = Product.objects.all()
        queryset = queryset.select_related('section')
        queryset = queryset.select_related('category')
        queryset = queryset.prefetch_related('size')
        queryset = queryset.prefetch_related('colors')
        queryset = queryset.prefetch_related('images')
        queryset = queryset.filter(isPublished=True, section__isPublished=True)
        return queryset


class SectionListAPI(generics.ListAPIView):
    '''Все разделы товаров'''
    queryset = Sections.objects.all()
    serializer_class = SectionsSerializer


class ProductBySectionListAPI(generics.ListAPIView):
    '''Товары определенного раздела'''
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductBySectionFilter

    def get_queryset(self, **kwargs):
        queryset = Product.objects.all()
        queryset = queryset.select_related('section')
        queryset = queryset.select_related('category')
        queryset = queryset.prefetch_related('size')
        queryset = queryset.prefetch_related('colors')
        queryset = queryset.filter(isPublished=True, section__isPublished=True, section__id = self.kwargs['pk'])

        return queryset



class SectionFiltersListAPI(APIView):
    '''API для создания фильта страницы Section'''

    def get(self, request, *args, **kwargs):
        sizes = Sizes.objects.all()
        colors = Colors.objects.all()
        categories = Categories.objects.filter(isPublished=True)

        sizes_serializer = SizesSerializer(sizes, many=True)
        colors_serializer = ColorSerializer(colors, many=True)
        categories_serializer = CategoriesSerializer(categories, many=True)

        data = {
            'sizes': sizes_serializer.data,
            'colors': colors_serializer.data,
            'categories': categories_serializer.data
        }

        return Response(data)


class ItemByFiltersAPI(APIView):

    def get(self, request, pk, *args, **kwargs):
        # Получаем параметры из запроса
        color_id = request.query_params.get('color', None)
        size_id = request.query_params.get('size', None)

        try:
            # Ищем конкретный товар по ID продукта, цвету и размеру. Он всегда один!
            item = Item.objects.filter(product=pk, color=color_id, size=size_id)

            if item:
                # Если товар найден и параметры совпадают, возвращаем его данные
                serializer = ItemSerializer(item, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise Item.DoesNotExist

        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
