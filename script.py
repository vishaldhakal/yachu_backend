import os
import django

# Setup Django environment FIRST, before any model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yachu.settings')
django.setup()


from orders.models import Order
from about.models import Franchise
# Now import your models AFTER Django is set up

# Use the correct field: slug or name
franchise_slug = "sankhamul"

try:
    franchise = Franchise.objects.get(slug=franchise_slug)
except Franchise.DoesNotExist:
    print(f"Franchise with slug '{franchise_slug}' does not exist.")
    exit(1)

# Assign to all orders (remove .filter(franchise__isnull=True) if you want to overwrite all)
orders = Order.objects.all()
updated_count = 0

for order in orders:
    order.franchise = franchise
    order.save()
    updated_count += 1

print(f"Updated {updated_count} orders to have franchise '{franchise_slug}'.")
