
from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
