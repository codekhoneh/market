import token
from django.shortcuts import render, redirect, reverse 
from django.views import View 
from django.contrib.auth import authenticate, login 
from django.contrib import messages 
from random import randint 
from django.utils import timezone 
from uuid import uuid4 
import ghasedakpack 
from account_app.models import OTP 
from account_app.forms import LoginForm, RegisterForm, CheckOTPForm 
from django.contrib.auth import get_user_model 
from datetime import timedelta
User = get_user_model()
SMS = ghasedakpack.Ghasedak("141f3512732f7ad303ef62d60421f851981825c2444dfbecc39de20fffa11cb42ZKQooAgRMAindor")
class UserRegister(View): 
    def get(self, request): 
        form = RegisterForm()
        return render(request, "account_app/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user, created = User.objects.get_or_create(phone=cd['phone'])

            if created:
                # اگر کاربر جدید بود
                user.set_password(cd['password'])
                user.save()

                randcode = randint(1000, 9999)
                token = str(uuid4())
                OTP.objects.create(phone=cd['phone'], code=randcode, token=token)

                SMS.verification({
                    'receptor': cd['phone'],
                    'type': '1',
                    'template': 'randcode',
                    'param1': randcode
                })
                messages.success(request, "کد تایید به شماره شما ارسال شد")
                print("OTP code:", randcode)
                return redirect(reverse('account_app:check-otp') + f'?token={token}')
            else:
                # اگر کاربر از قبل وجود داشت
                messages.info(request, "شما قبلاً ثبت‌نام کرده‌اید")
                # return redirect(reverse('home:main'))  # صفحه‌ی home

        return render(request, "account_app/register.html", {"form": form})

class CheckOTPView(View): 
    def get(self, request): 
        token = request.GET.get('token')
        form = CheckOTPForm()
        
        # بررسی اینکه آیا کد منقضی است
        is_expired = False
        try:
            otp = OTP.objects.get(token=token)
            is_expired = otp.is_expired()
        except OTP.DoesNotExist:
            pass
        
        return render(request, "account_app/check-otp.html", {
            "form": form, 
            "token": token,
            "is_expired": is_expired
        }) 
 
    def post(self, request): 
        token = request.GET.get('token')  
        form = CheckOTPForm(request.POST) 
        if form.is_valid(): 
            cd = form.cleaned_data
            try: 
                otp = OTP.objects.get(code=cd['code'], token=token) 
            except OTP.DoesNotExist: 
                form.add_error(None, "کد تایید معتبر نیست") 
                return render(request, "account_app/check-otp.html", {"form": form, "token": token})
            
            # بررسی منقضی بودن کد
            if otp.is_expired():
                otp.delete()
                randcode = randint(1000, 9999)
                new_token = str(uuid4())
                OTP.objects.create(phone=otp.phone, code=randcode, token=new_token)

                try:
                    SMS.verification({
                        'receptor': otp.phone,
                        'type': '1',
                        'template': 'randcode',
                        'param1': randcode
                    })
                except Exception as e:
                    print(f"SMS Error: {e}")
                
                messages.warning(request, "کد منقضی شده است. کد جدید برای شما ارسال شد")
                print("New OTP code:", randcode)
                return redirect(reverse('account_app:check-otp') + f'?token={new_token}')
 
            # کاربر را بررسی کن یا ایجاد کن
            user, is_create = User.objects.get_or_create(phone=otp.phone) 
            if is_create: 
                user.set_unusable_password() 
                user.save() 
 
            login(request, user) 
            otp.delete() 
            messages.success(request, "ثبت‌نام/ورود شما موفقیت‌آمیز بود")
            return redirect('home:main') 
 
        return render(request, "account_app/check-otp.html", {"form": form, "token": token})

class ResendOTPView(View):
    def get(self, request):
        token = request.GET.get('token')
        
        try:
            otp = OTP.objects.get(token=token)
        except OTP.DoesNotExist:
            messages.error(request, "توکن نامعتبر است")
            return redirect('account_app:register')
        
        # حذف کد قدیمی و ایجاد کد جدید
        otp.delete()
        randcode = randint(1000, 9999)
        new_token = str(uuid4())
        OTP.objects.create(phone=otp.phone, code=randcode, token=new_token)
        
        # ارسال SMS
        try:
            SMS.verification({
                'receptor': otp.phone,
                'type': '1',
                'template': 'randcode',
                'param1': randcode
            })
            messages.success(request, "کد جدید برای شما ارسال شد")
        except Exception as e:
            print(f"SMS Error: {e}")
            messages.warning(request, "خطا در ارسال SMS - کد در کنسول نمایش داده شد")
        
        print("New OTP code:", randcode)
        return redirect(reverse('account_app:check-otp') + f'?token={new_token}')

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
