import requests
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Customer, Order, Products, Item
from django.http import JsonResponse

def send_order_to_telegram(data, order):
    """Функция дублирует сделанный заказ в тг бота"""
    TG_TOKEN = os.environ.get('TG_TOKEN')
    CHAT_ID = 1357174078

    # Сбор данных о заказе
    customer_data = data['Customer']
    name = customer_data['Name']
    phone = customer_data['Phone']
    address = customer_data['Address']
    comment = customer_data['Comment']
    total_price = data['TotalPrice']

    # Сбор данных о товарах
    items_list = []
    for item_data in data['Items']:
        item = Item.objects.get(
            product=item_data['id'],
            color=item_data['color']['id'],
            size=item_data['size']['id']
            )
        items_list.append(f"ID: {item.id}, Название: {item}, Цвет: {item.color}, Размер: {item.size}, Колличество: {item_data['quantity']}")
    items_text = '\n'.join(items_list)

    # Тело сообщения
    message = (
        f"Новый заказ №{order}\n"
        f"Заказчик: {name}\n"
        f"Телефон: {phone}\n"
        f"Адрес: {address}\n"
        f"Комментарий: {comment}\n"
        f"Товары: {items_text}\n"
        f"Общая сумма: {total_price}"
    )

    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
    }

    requests.post(url, data=payload)

    # Телефон заказчика
    url_phone = f"https://api.telegram.org/bot{TG_TOKEN}/sendContact"
    payload_phone = {
        'chat_id': CHAT_ID,
        'phone_number': ''.join(filter(str.isdigit, phone)), # +7 (123) 456-78-90  -> 7123456790
        'first_name': name,
    }

    requests.post(url_phone, data=payload_phone)


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

        send_order_to_telegram(data, order)

        return JsonResponse({'message': 'Order created successfully'}, status=201)