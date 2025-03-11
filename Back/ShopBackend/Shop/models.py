from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за штуку')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Основное фото продукта')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    section = models.ForeignKey('Sections', on_delete=models.CASCADE, verbose_name='Раздел сайта')
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, verbose_name='Категория')
    size = models.ManyToManyField('Sizes', verbose_name='Размер одежды')
    colors = models.ManyToManyField('Colors', verbose_name='Цвет')
    isPublished = models.BooleanField(default=True, verbose_name='Отображение продукта на сайте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Одежда'
        verbose_name_plural = 'Вещи'
        ordering = ('-pk',)


class Sizes(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Размер одежды')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер одежды'
        verbose_name_plural = 'Размеры одежды'


class Colors(models.Model):
    name = models.CharField(max_length=100, verbose_name='Цвет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Sections(models.Model):
    name = models.CharField(max_length=255, verbose_name='Раздел')
    isPublished = models.BooleanField(default=True, verbose_name='Отображение раздела на сайте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ('pk',)


class Categories(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории которое будет отображаться на сайте')
    isPublished = models.BooleanField(default=True, verbose_name='Отображение категории на сайте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('pk',)



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='images')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')

    def __str__(self):
        return f"Фото {self.product.name}"

    class Meta:
        verbose_name = 'Дополнительное фото продукта'
        verbose_name_plural = 'Дополнительные фото продуктов'


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Конкретный товар')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, verbose_name='Цвет')
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE, verbose_name='Размер')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество товара')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Конкретный товар'
        verbose_name_plural = 'Конкретные товары'
