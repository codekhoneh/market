from django.shortcuts import render,redirect,get_object_or_404
from django.views import View 
from order_app import views 
from product_app.models import Product
from order_app.order_madul  import Order
from order_app.models import Buy, BuyItem
from django.contrib.auth.mixins import LoginRequiredMixin
class OrderDetailView(View):
    def get(self, request):
        cart = Order(request)

        return render(request, "order_app/order_detail.html", {
            "cart": cart
        })

class OrderAddView(View): 
    
     
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity', 1)

        cart = Order(request)
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

# Create your views here.
