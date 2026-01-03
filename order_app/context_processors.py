from .order_madul import Order

def cart_processor(request):
    return {
        'cart': Order(request)
    }
