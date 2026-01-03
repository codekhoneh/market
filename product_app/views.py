from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from django.views import View
from order_app.models import Cart, CartItem
from django.contrib import messages


class ProductListView(ListView):
    model = Product
    template_name = "product_app/product_list.html"
    context_object_name = "products"
    paginate_by = 3


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_app/product_detail.html"
    context_object_name = "product_d"
    slug_field = "slug"
    slug_url_kwarg = "slug"

class AddToCartView(View):
    def post(self, request, product_slug):
        # گرفتن محصول با استفاده از slug
        product = get_object_or_404(Product, slug=product_slug)
        
        # دریافت یا ایجاد سبد خرید برای کاربر وارد شده یا جلسه (session)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key, is_active=True)
        
        # چک کردن اینکه آیا محصول قبلاً در سبد خرید وجود دارد یا نه
        # هنگام ایجاد آیتم جدید، مقدار `price` را در defaults قرار می‌دهیم
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"price": product.price},
        )
        
        # اگر محصول قبلاً وجود دارد، تعداد آن را افزایش می‌دهیم
        if not created:
            cart_item.quantity += 1
        
        # اختصاص قیمت محصول به price
        cart_item.price = product.price 
        cart_item.save()  # ذخیره تغییرات
        # نمایش پیام موفقیت
        messages.success(request, 'پیغام شما با موفقیت ثبت شد')

        # بازگشت به صفحه قبلی یا صفحه محصول
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('product_list')

