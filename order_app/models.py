from django.db import models
from django.conf import settings
from product_app.models import Product
# Create your models here. 
from django.db import models 
# from django.contrib.auth.models import User 
class Order(models.Model): 
    user = models.ForeignKey( 
    settings.AUTH_USER_MODEL, 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True 
)   
    full_name = models.CharField(max_length=100) 
    phone = models.CharField(max_length=20) 
    address = models.TextField() 
    subtotal = models.PositiveIntegerField() 
    discount = models.PositiveIntegerField(default=0) 
    shipping = models.PositiveIntegerField(default=0) 
    total = models.PositiveIntegerField() 
    is_paid = models.BooleanField(default=False) 
    created = models.DateTimeField(auto_now_add=True) 
 
 
    def __str__(self): 
        return f"Order #{self.id}"
class OrderItem(models.Model): 
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    price = models.PositiveIntegerField() 
    quantity = models.PositiveIntegerField() 
    color = models.CharField(max_length=50, blank=True, null=True) 
    size = models.CharField(max_length=50, blank=True, null=True) 
    def __str__(self): 
        return self.product.title 
# Create your models here.
