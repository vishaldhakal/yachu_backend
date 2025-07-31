from django.db import models
from django.contrib.auth import get_user_model
from about.models import Franchise

User = get_user_model()


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    PRODUCT_CHOICES = [
        ('Dandruff Oil', 'Dandruff Oil'),
        ('Hairfall Oil', 'Hairfall Oil'),
        ('Baldness Oil', 'Baldness Oil'),
        ('Shampoo Bottle', 'Shampoo Bottle'),
        ('Shampoo Sachet', 'Shampoo Sachet')
    ]
    name = models.CharField(max_length=255, choices=PRODUCT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('home.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    franchise = models.ForeignKey(
        Franchise, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    delivery_address = models.CharField(max_length=200)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    alternate_phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    order_status = models.CharField(
        max_length=255, choices=ORDER_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} - {self.order_status}'


class Commission(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name='commissions')
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller} - ₹{self.amount} - {'Paid' if self.paid else 'Unpaid'}"

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.order.total_amount * \
                (self.seller.commission_rate / 100)
        super().save(*args, **kwargs)


class Tracking(models.Model):
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.details}"
