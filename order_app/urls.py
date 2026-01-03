from django.urls import path

# register app namespace for reversing with 'order_app:...'
app_name = 'order_app'
from .views import CartDetailView,CartItemIncreaseView,CartItemDecreaseView,CartItemRemoveView

urlpatterns = [
    path('',CartDetailView.as_view(),name='order'),
    path('increase/<int:item_id>/', CartItemIncreaseView.as_view(), name='cart_item_increase'),
    path('decrease/<int:item_id>/', CartItemDecreaseView.as_view(), name='cart_item_decrease'),
    path('remove/<int:item_id>/', CartItemRemoveView.as_view(), name='cart_item_remove'),
]