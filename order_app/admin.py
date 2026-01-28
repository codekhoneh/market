from django.contrib import admin 
from . import models 
 
from django.contrib import admin 
from .models import Order, OrderItem 
 
class OrderItemInline(admin.TabularInline): 
    model = OrderItem 
    extra = 0 
 
@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin): 
    list_display = ('id', 'full_name', 'is_paid', 'created') 
    list_filter = ('is_paid', 'created') 
    inlines = [OrderItemInline]
# Register your models here.
