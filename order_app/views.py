from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart,CartItem
from django.http import Http404

class CartDetailView(View):
    def get(self, request):
        """
        این متد فقط مسئول «نمایش» سبد خرید است
        هیچ داده‌ای را تغییر نمی‌دهد
        """

        # اگر کاربر لاگین کرده باشد
        if request.user.is_authenticated:

            # گرفتن یا ساخت سبد خرید فعال برای کاربر
            cart, created = Cart.objects.get_or_create(
                user=request.user,
                is_active=True
            )

        # اگر کاربر لاگین نکرده باشد
        else:
            # اطمینان از وجود session
            if not request.session.session_key:
                request.session.create()

            session_key = request.session.session_key

            # گرفتن یا ساخت سبد خرید فعال بر اساس session
            cart, created = Cart.objects.get_or_create(
                session_key=session_key,
                is_active=True
            )
        # ارسال cart به template
        context = {"cart": cart}

        return render(request, "order_app/cart.html", context)
@method_decorator(csrf_exempt, name='dispatch')
class CartItemRemoveView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user, is_active=True)
        else:
            if not request.session.session_key:
                raise Http404
            cart = get_object_or_404(Cart, session_key=request.session.session_key, is_active=True)

        if cart_item.cart != cart:
            raise Http404
        cart_item.delete()
        return redirect('order_app:order')
    
@method_decorator(csrf_exempt, name='dispatch')
class CartItemDecreaseView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user, is_active=True)
        else:
            if not request.session.session_key:
                raise Http404
            cart = get_object_or_404(Cart, session_key=request.session.session_key, is_active=True)

        if cart_item.cart != cart:
            raise Http404

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    
        # برگشت به صفحه سبد خرید
        return redirect("order_app:order")
    
@method_decorator(csrf_exempt, name='dispatch')
class CartItemIncreaseView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user, is_active=True)
        else:
            if not request.session.session_key:
                raise Http404
            cart = get_object_or_404(Cart, session_key=request.session.session_key, is_active=True)

        if cart_item.cart != cart:
            raise Http404

        cart_item.quantity += 1
        cart_item.save()
        
        # برگشت به صفحه سبد خرید
        return redirect('order_app:order')

