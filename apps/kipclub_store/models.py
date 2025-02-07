from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.IntegerField(verbose_name="Количество на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders", verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"
