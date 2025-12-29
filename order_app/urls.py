from django.urls import path 
from .views import OrderDetailView,OrderAddView,OrderDeleteView
app_name='order' 
urlpatterns=[path('detail/',OrderDetailView.as_view(),name='order_detail'),
             path('add/<int:pk>/', OrderAddView.as_view(), name='order_add'),
             path('delete/<str:id>/', OrderDeleteView.as_view(), name='order_delete'), 
             ]