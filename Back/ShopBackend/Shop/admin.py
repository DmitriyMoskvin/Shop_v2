from django.contrib import admin
from .models import Product, Sizes, Sections, Categories, Colors, ProductImage, Item

admin.site.register(Product)
admin.site.register(Sizes)
admin.site.register(Sections)
admin.site.register(Categories)
admin.site.register(Colors)
admin.site.register(ProductImage)
admin.site.register(Item)