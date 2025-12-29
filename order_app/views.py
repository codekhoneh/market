from django.shortcuts import render,redirect,get_object_or_404
from django.views import View 
from order_app import views 
from product_app.models import Product
from order_app.order_madul  import Order
class OrderDetailView(View):
    def get(self, request):
        cart = Order(request)

        return render(request, "order_app/order_detail.html", {
            "cart": cart
        })

class OrderAddView(View): 
    def get(self, request): 
        return render(request,"order_app/order_detail.html", {}) 
     
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
# Create your views here.
