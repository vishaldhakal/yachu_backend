from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

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
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def get_total_price(self):
        return (self.product.price * self.quantity) * (1 - self.discount / 100)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Prepaid', 'Prepaid')
    ]

    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, related_name='orders')
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=True)
    delivery_address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20)
    alternate_phone_number = models.CharField(max_length=20, blank=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f'{self.full_name} - {self.order_status}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.total_amount = self.delivery_charge
        else:
            self.total_amount = sum(op.get_total_price() for op in self.order_products.all()) + self.delivery_charge
        if is_new:
            super().save(update_fields=['total_amount'])

class Commission(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='commissions')
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller} - ₹{self.amount} - {'Paid' if self.paid else 'Unpaid'}"

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.order.total_amount * (self.seller.commission_rate / 100)
        super().save(*args, **kwargs)
