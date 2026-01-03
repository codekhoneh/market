from django.db import models
from django.conf import settings
from product_app.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    SHIPPING_COST = 10

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_price(self):
        return self.subtotal + self.SHIPPING_COST


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def total_price(self):
        return self.quantity * self.price
