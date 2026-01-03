from django.db import models
from django.conf import settings
from product_app.models import Product
class  Buy(models.Model): 
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='buy') 
    address=models.CharField(max_length=300) 
    email=models.EmailField(blank=True,null=True) 
    phone=models.CharField(max_length=12) 
    craeted_add=models.DateTimeField(auto_now_add=True) 
    is_paid=models.BooleanField(default=False) 
    def __str__(self):
     return f"Buy {self.id} - {self.user}"

class BuyItem(models.Model): 
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='buy_items')
    size = models.CharField(max_length=12) 
    color = models.CharField(max_length=12) 
    quantity = models.SmallIntegerField(default=1) 
    price = models.PositiveIntegerField() 
 
 
 
    def __str__(self): 
        return f'{self.product.title} x{self.quantity} ({self.color}/{self.size})' 
    @property 
    def total_price(self): 
        return self.price * self.quantity 
# Create your models here.
