from django.urls import path 
from .views import OrderDetailView,OrderAddView,OrderDeleteView, OrderSuccessView ,OrderItemIncreaseView ,OrderItemDecreaseView
# OrderHistoryView , CheckoutView,
app_name='order' 
urlpatterns=[path('detail/',OrderDetailView.as_view(),name='order_detail'),
             path('add/<int:pk>/', OrderAddView.as_view(), name='order_add'),
             path('delete/<str:id>/', OrderDeleteView.as_view(), name='order_delete'),
             path('success/', OrderSuccessView.as_view(), name='order_success'),
            #  path('checkout/', CheckoutView.as_view(), name='checkout'),
             path('item/increase/<str:id>/', OrderItemIncreaseView.as_view(), name='order_item_increase'),
             path('item/decrease/<str:id>/', OrderItemDecreaseView.as_view(), name='order_item_decrease'),
            #  path('my-orders/', OrderHistoryView.as_view(), name='order_history'),
             ]