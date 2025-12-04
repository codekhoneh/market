from django.urls import path 
from .views import UserRegister, UserLogin, CheckOTPView, ResendOTPView
app_name='account_app' 
urlpatterns = [ 
    path("login/", UserLogin.as_view(), name="login"), 
    path('check-otp/', CheckOTPView.as_view(), name='check-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path("register/", UserRegister.as_view(), name="register"),
] 
 