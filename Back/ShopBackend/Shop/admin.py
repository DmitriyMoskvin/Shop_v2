from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Sizes, Sections, Categories, Colors, ProductImage, Item

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('photo_tag', 'name', 'description', 'price_per_unit', 'section', 'category', 'isPublished', 'get_sizes', 'get_colors')
    list_editable = ('price_per_unit', 'isPublished')
    list_per_page = 10
    search_fields = ('name',)
    list_filter = ('isPublished',)

    filter_horizontal = ('size', 'colors')

    @admin.display(description='Размеры')
    def get_sizes(self, obj):
        return [size.name for size in obj.size.all()]

    @admin.display(description='Цвета')
    def get_colors(self, obj):
        return [color.name for color in obj.colors.all()]

    @admin.display(description='Фото')
    def photo_tag(self, obj):
        return format_html(f'<img src="{obj.photo.url}" style="width: 50px;" />')

@admin.register(Sections)
class SectionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'isPublished')
    list_editable = ('isPublished', )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'isPublished')
    list_editable = ('isPublished', )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'quantity')


admin.site.register(Sizes)
admin.site.register(Colors)
admin.site.register(ProductImage)
