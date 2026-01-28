from django.shortcuts import render,redirect,get_object_or_404
from django.views import View 
from order_app import views 
from product_app.models import Product
from order_app.order_madul  import Order
from order_app.models import Order,OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from order_app.forms import CheckoutForm
# from .models import Order as OrderModel 
from order_app.order_madul import Order as Cart 
class OrderDetailView(View):
    def get(self, request): 
        cart = Cart(request) 
        subtotal = cart.subtotal 
        discount = cart.discount_amount 
        has_discount = discount > 0 
        shipping = 10 if subtotal > 0 else 0 
        total = subtotal - discount + shipping 
 
        return render(request, "order_app/order_detail.html", { 
            "cart": cart, 
            "subtotal": subtotal, 
            "discount": discount, 
            "has_discount": has_discount, 
            "shipping": shipping, 
            "total": total, 
        })

class OrderAddView(View): 
    
     
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity', 1)

        cart = Cart(request)
        cart.add(product, quantity, color, size)

        return redirect('order:order_detail')
  # یا هر صفحه‌ای که داری
class OrderDeleteView(View): 
    def get(self, request, id): 
        cart = Order(request) 
        cart.delete(id)   # اب متیآ فذح unique_id 
        return redirect('order:order_detail')
# class CheckoutView(LoginRequiredMixin,View):
#     login_url = '/accounts/login/'

#     def get(self, request):
#         cart = Order(request)
#         return render(request, 'order_app/checkout.html', {'cart': cart})
#     def post(self, request):
#         cart = Order(request)

#         if not list(cart):
#             return redirect('order:order_detail')

#         buy = Buy.objects.create(
#             user=request.user,
#             address=request.POST.get('address'),
#             phone=request.POST.get('phone'),
#             email=request.POST.get('email')
#         )

#         for item in cart:
#             BuyItem.objects.create(
#                 buy=buy,
#                 product=item['product_d'],
#                 size=item['size'],
#                 color=item['color'],
#                 quantity=item['quantity'],
#                 price=item['price']
#             )

#         cart.clear()

#         return redirect('order:order_detail')

class OrderSuccessView(View):
    def get(self, request):
        return render(request, 'order_app/order_success.html')
class OrderItemIncreaseView(View):
    def get(self, request, id):
        cart = Order(request)
        cart.increase(id)
        return redirect('order:order_detail')


class OrderItemDecreaseView(View):
    def get(self, request, id):
        cart = Order(request)
        cart.decrease(id)
        return redirect('order:order_detail')

def apply_discount(request): 
    if request.method == 'POST': 
        cart = Cart(request) 
        code = request.POST.get('code') 
 
        # هداس هنومن 
        if code == 'OFF10':# خت دک یدصرد هاوخلد فیف 
            cart.apply_discount('percent', 10) 
        elif code == 'OFF500': 
            cart.apply_discount('fixed', 500)# غلبم هاوخلد فیفخت دک تباث 
 
    return redirect('order:order_detail')
def remove_discount(request): 
    cart = Cart(request) 
    cart.remove_discount() 
    return redirect('order:order_detail') 
class CheckoutView(View): 
    def get(self, request): 
        cart = Cart(request) 
 
        # هب درگرب ،تسا یلاخ دبس رگا cart 
        if cart.subtotal== 0: 
            return redirect('order:order_detail') 
 
        form = CheckoutForm() 
        return render(request, 'order_app/checkout.html', { 
            'cart': cart, 
            'form': form, 
        }) 
 
    def post(self, request): 
 

 
        cart = Cart(request) 
        form = CheckoutForm(request.POST) 
 
        # تسا ربتعمان مرف رگا 
        if not form.is_valid(): 
            return render(request, 'order_app/checkout.html', { 
                'cart': cart, 
                'form': form, 
            }) 
 
        subtotal = cart.subtotal 
        discount = cart.discount_amount 
        shipping = 10 if subtotal > 0 else 0 
        total = subtotal - discount + shipping 
        # شرافس تخاس 
        order = Order.objects.create( 
            user=request.user if request.user.is_authenticated else None, 
            full_name=form.cleaned_data['full_name'], 
            phone=form.cleaned_data['phone'], 
            address=form.cleaned_data['address'], 
            subtotal=subtotal, 
            discount=discount, 
            shipping=shipping, 
            total=total, 
        ) 
        # متیآ هریخذ اه 
        for item in cart: 
            OrderItem.objects.create( 
                order=order, 
                product=item['product_d'], 
                price=item['price'], 
                quantity=item['quantity'], 
                color=item.get('color'), 
                size=item.get('size'), 
            ) 
        # دیرخ دبس ندرک یلاخ 
        request.session.pop('cart', None) 
        request.session.pop('discount', None) 
        request.session.modified = True 
        return redirect('order:order_success', order_id=order.id)
def  order_success(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,'order_app/success_order.html',{'order':order})
# Create your views here.
