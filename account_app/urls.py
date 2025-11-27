from django.urls import path 
from account_app.views import UserLogin 
app_name='account' 
urlpatterns = [ 
    path("login/", UserLogin.as_view(), name="login"), 
] 
 