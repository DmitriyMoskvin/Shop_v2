from django.urls import path

from Basket.views import OrdersApi, TestOrdersApi

urlpatterns = [
    path('Orders/', TestOrdersApi.as_view(), name='orders'),
]