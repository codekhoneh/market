from django.shortcuts import render, redirect 
from django.views import View 
from django.contrib.auth import authenticate, login 
from .forms import LoginForm 
 

class UserLogin(View): 
    def get(self, request): 
        form = LoginForm() 
        return render(request, "account_app/login.html", {"form": form}) 
 
    def post(self, request): 
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            phone = form.cleaned_data["phone"] 
            password = form.cleaned_data["password"] 
 
            user = authenticate(request, username=phone, password=password) 
            if user is not None: 
                login(request, user) 
                return redirect("home:main") 
            else: 
                form.add_error(None, "نام کاربری یا رمز عبور اشتباه است") 
        return render(request, "account_app/login.html", {"form": form}) 
# Create your views here.
