from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from django.http import JsonResponse

from .serializers import OrdersApiSerializer
import io
from rest_framework.parsers import JSONParser

class OrdersApi(APIView):
    def post(self, request):
        print(request.data)
        print(type(request.data))
        return Response('data', status=status.HTTP_200_OK)


class TestOrdersApi(APIView):
    def post(self, request):

        # Парсим JSON из запроса
        data = request.data

        # 1. Создаем заказчика
        customer_data = data['Customer']
        customer = Customer.objects.create(
            name=customer_data['Name'],
            phone=customer_data['Phone'],
            address=customer_data['Address'],
            comment=customer_data['Comment']
        )

        # 2. Создаем заказ
        order = Order.objects.create(
            customer=customer,
            total_price=data['TotalPrice']
        )


        # 3. Создаем товары в заказе
        for item_data in data['Items']:

            try:
                item = Item.objects.get(product=item_data['id'], color=item_data['color']['id'], size=item_data['size']['id'])

                Products.objects.create(
                    item=item,
                    selected_quantity=item_data['quantity'],
                    order=order
                )
            except Item.DoesNotExist:
                return JsonResponse({'error': f"Item with id {item_data['id']} not found"}, status=400)

        return JsonResponse({'message': 'Order created successfully'}, status=201)