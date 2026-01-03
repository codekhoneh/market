from order_app.models import Cart

def cart_item_count(request):
    """
    این context processor تعداد اقلام سبد خرید را برمی‌گرداند.
    """
    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        cart_item_count = cart.items.count()
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            is_active=True
        )
        cart_item_count = cart.items.count()
    
    return {'cart_item_count': cart_item_count}