from django.contrib import admin
from .models import Product, Size, Color, ProductImage, Information


class InformationInline(admin.StackedInline):
    model = Information
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    inlines = (InformationInline,)


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductImage)
