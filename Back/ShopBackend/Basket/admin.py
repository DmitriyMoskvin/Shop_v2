from django.contrib import admin
from .models import Customer, Order, Products

class ProductsInline(admin.TabularInline):
    model = Products
    extra = 0


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'comment')
    search_fields = ('name', 'phone')
    inlines = [OrderInline,]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'time_create')
    list_filter = ('customer', 'time_create')
    search_fields = ('customer__name',)
    inlines = [ProductsInline]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('item', 'selected_quantity', 'order',)
    list_filter = ('order',)
