from django.contrib import admin 
from . import models 
 
class BuyItemInline(admin.TabularInline): 
    model = models.BuyItem 
    # extra = 0  اختیاری است تعداد فرم خالی
@admin.register(models.Buy) 
class BuyAdmin(admin.ModelAdmin): 
    list_display = ('user', 'address', 'phone', 'is_paid') 
    list_filter = ('is_paid',)  # دشاب هتشاد اماک ً امتح 
    inlines = (BuyItemInline,)
# Register your models here.
