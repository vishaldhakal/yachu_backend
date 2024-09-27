from django.db import models

# Create your models here.
class Product(models.Model):
    OIL_CHOICES = [
        ('Dandruff Case', 'Dandruff Case'),
        ('Hairfall Case', 'Hairfall Case'),
        ('Baldness Case', 'Baldness Case'),
        ('Shampoo Bottle', 'Shampoo Bottle'),
        ('Shampoo sashe pack of 10', 'Shampoo sashe pack of 10')
    ]
    name = models.CharField(max_length=255, choices=OIL_CHOICES)
    price = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Prepaid', 'Prepaid')
    ]
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    delivery_location = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.IntegerField()
    alternate_phone_number = models.IntegerField(blank=True, null=True)
    delivery_charge = models.IntegerField(default=0,blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    convinced_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='convinced_by')
    payment_method = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES)
    shampoo = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name} - {self.order_status}'
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            # For new instances, save first to get a primary key
            super().save(*args, **kwargs)
            self.calculate_total_amount()
            super().save(update_fields=['total_amount'])
        else:
            # For existing instances, calculate total before saving
            self.calculate_total_amount()
            super().save(*args, **kwargs)

    def calculate_total_amount(self):
        product_total = sum(product.price for product in self.order_products.all())
        self.total_amount = product_total + (self.delivery_charge or 0)
