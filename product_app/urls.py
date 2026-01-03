
from django.urls import path
from .views import ProductListView, ProductDetailView,AddToCartView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart/<slug:product_slug>',AddToCartView.as_view(),name='add_to_cart')
]
