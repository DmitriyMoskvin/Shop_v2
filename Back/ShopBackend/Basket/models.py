from django.db import models
from Shop.models import Item

class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя заказчика')
    phone = models.CharField(max_length=18, verbose_name='Телефонный номер заказчика')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    comment = models.TextField(verbose_name='Коментарий к заказу')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = ('-pk',)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Заказчик')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    total_price = models.PositiveIntegerField(verbose_name='Общая сумма заказа')

    def __str__(self):
        return str(self.pk)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-pk',)


class Products(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Конкретный товар')
    selected_quantity = models.PositiveSmallIntegerField(verbose_name='Количество товара которое заказал заказчик')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')

    def __str__(self):
        return str(self.pk)


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
