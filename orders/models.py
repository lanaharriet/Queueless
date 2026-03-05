from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='menu_images/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    token_number = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"