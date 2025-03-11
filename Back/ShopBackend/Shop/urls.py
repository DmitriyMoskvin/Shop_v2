from django.urls import path

from Shop.views import ProductListAPI, ProductDetailAPI, SectionListAPI, ProductBySectionListAPI, SectionFiltersListAPI, ItemByFiltersAPI

urlpatterns = [
    path('product/<pk>/', ProductDetailAPI.as_view(), name='product_detail'),
    path('products/', ProductListAPI.as_view(), name='product_list'),
    path('section/<pk>/', ProductBySectionListAPI.as_view(), name='product_by_section_list'),
    path('sections/', SectionListAPI.as_view(), name='section_list'),
    path('filters/', SectionFiltersListAPI.as_view(), name='section_filters_list'),
    path('item/<pk>/', ItemByFiltersAPI.as_view()),
]