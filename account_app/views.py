from django.shortcuts import render, redirect, reverse 
from django.views import View 
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages 
from random import randint 
from django.utils import timezone 
from uuid import uuid4 
import ghasedakpack 
from account_app.models import OTP 
from account_app.forms import LoginForm, RegisterForm, CheckOTPForm, fa_to_en_digits
from django.contrib.auth import get_user_model 
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_email_otp
 
User = get_user_model()
SMS = ghasedakpack.Ghasedak("141f3512732f7ad303ef62d60421f851981825c2444dfbecc39de20fffa11cb42ZKQooAgRMAindor")
class UserRegister(View): 
    def get(self, request): 
        form = RegisterForm()
        return render(request, "account_app/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid(): 
            return render(request, "account_app/register.html", {"form": form})
        cd = form.cleaned_data 
        phone = cd.get("phone") 
        email = cd.get("email") 
        password = cd.get("password") 
        existing_user = None 
        if phone: 
            existing_user = User.objects.filter(phone=phone).first() 
        elif email: 
            existing_user = User.objects.filter(email=email).first()
        if existing_user: 
            messages.info(request, "شما قبلا ثبت نام کرده اید. لطفا وارد شوید") 
            return redirect("account_app:login")
        randcode = randint(1000, 9999) 
        otp_token = str(uuid4()) 
        OTP.objects.create( 
            phone=phone, 
            email=email, 
            code=str(randcode), 
            token=otp_token, 
            password=password 
        ) 
        print(f"🔐 OTP Code: {randcode}")
        try: 
            if phone: 
                print(f"📱 ارسال کد به شماره: {phone}") 
                SMS.verification({ 
                    'receptor': phone, 
                    'type': '1', 
                    'template': 'randcode', 
                    'param1': randcode 
                }) 
                messages.success(request, "کد تایید به شماره شما ارسال شد") 
            elif email: 
                print(f"📧 ارسال کد به ایمیل: {email}") 
                send_email_otp(email, randcode) 
                messages.success(request, "کد تایید به ایمیل شما ارسال شد") 
        except Exception as e: 
            print(f"❌ Error: {e}") 
            messages.warning(request, "خطا در ارسال کد") 
 
        return redirect(reverse("account_app:check-otp") + f"?token={otp_token}")

class CheckOTPView(View): 
    def get(self, request): 
        token = request.GET.get('token')
        form = CheckOTPForm()
        otp = OTP.objects.filter(token=token).first() 
        # بررسی اینکه آیا کد منقضی است
        is_expired =  otp.is_expired() if otp else False
        # try:
        #     otp = OTP.objects.get(token=token)
        #     is_expired = otp.is_expired()
        # except OTP.DoesNotExist:
        #     pass
        
        return render(request, "account_app/check-otp.html", {
            "form": form, 
            "token": token,
            "is_expired": is_expired, 
            "otp_phone": otp.phone if otp else None, 
            "otp_email": otp.email if otp else None, 
        }) 
 
    def post(self, request): 
        token = request.GET.get('token')  
        form = CheckOTPForm(request.POST) 

        if not form.is_valid(): 
            return render(request, "account_app/check-otp.html", {"form": form, "token": token}) 
 
        code = form.cleaned_data["code"] 
        otp = OTP.objects.filter(token=token, code=code).first() 
 
        if not otp: 
            form.add_error(None, "کد تایید معتبر نیست") 
            return render(request, "account_app/check-otp.html", {"form": form, "token": token}) 
 
        if otp.is_expired(): 
            messages.warning(request, "کد تایید منقضی شده است.لطفا ارسال محدد بزنید") 
            return redirect(reverse("account_app:resend-otp") + f"?token={token}") 
 
        # ربراک نتخاس ای ندرک ادیپ 
        user = None 
        if otp.email: 
            user = User.objects.filter(email=otp.email).first() 
        if not user and otp.phone: 
            user = User.objects.filter(phone=otp.phone).first() 
 
        if not user: 
            user = User.objects.create( 
                email=otp.email, 
                phone=otp.phone or None, 
                full_name=otp.full_name or "" 
            ) 
 
        # زمر هریخذ usable 
        if otp.password: 
            user.set_password(otp.password) 
            user.save() 
 
        # دنچ یتقو Authentication backend هدش یدنبرکیپ دیاب ،دنا backend مینک صخشم ار 
        # ات Django مادک زا دنادب backend هدافتسا دورو یارب  دنک . 
        login(request, user, backend='account_app.backends.EmailOrPhoneBackend') 
        otp.delete() 
 
        messages.success(request, "ثبت نام / ورود شما موفقیت آمیز بود") 
        return redirect("home:main")
class ResendOTPView(View):
      def get(self, request): 
        token = request.GET.get("token") 
        otp = OTP.objects.filter(token=token).first() 
 
        if not otp: 
            messages.error(request, "تسا ربتعمان نکوت") 
            return redirect("account_app:register") 
 
        #  دیلوت  دیدج دک 
        randcode = randint(1000, 9999) 
        otp.code = str(randcode) 
        otp.created_at = timezone.now() 
        otp.save() 
 
        # لاسرا OTP دیدج 
        try: 
            if otp.phone: 
                print(f"📱 ارسال کد مجدد به شماره: {otp.phone}") 
                print(f"🔐 کد OTP: {randcode}") 
                SMS.verification({ 
                    'receptor': otp.phone, 
                    'type': '1', 
                    'template': 'randcode', 
                    'param1': randcode 
                }) 
                messages.success(request, "کد جدید به شماره شما ارسال شد") 
            elif otp.email: 
                print(f"📧 ارسال کد مجدد به ایمیل: {otp.email}") 
                print(f"🔐 کد OTP: {randcode}") 
                from utils import send_email_otp 
                send_email_otp(otp.email, randcode) 
                messages.success(request, "کد جدید به ایمیل شما ارسال شد") 
        except Exception as e: 
            print(f"Send Error: {e}") 
            messages.warning(request, "خطا در ارسال کد") 
 
        return redirect(reverse("account_app:check-otp") + f"?token={token}") 
class UserLogin(View): 
    def get(self, request): 
        form = LoginForm() 
        return render(request, "account_app/login.html", {"form": form}) 
 
    def post(self, request): 
        form = LoginForm(request.POST)  
        if not form.is_valid(): 
            print(f"❌ Form errors: {form.errors}")
            return render(request, "account_app/login.html", {"form": form}) 
 
        identifier = form.cleaned_data.get("identifier")
        password = form.cleaned_data.get("password") 
 
        print(f"🔍 Login attempt - identifier: {identifier}, password: {'*' * len(password) if password else 'None'}")
        
        user = authenticate(request, username=identifier, password=password) 
        print(f"🔑 Authentication result: {user}")
        
        if user is not None: 
            login(request, user, backend='account_app.backends.EmailOrPhoneBackend') 
            messages.success(request, "خوش آمدید!")
            return redirect("home:main") 

        form.add_error(None, "ایمیل یا شماره تلفن یا رمز عبور اشتباه است") 
        return render(request, "account_app/login.html", {"form": form}) 
class UserLogout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "خروج موفقیت‌آمیز بود")
        return redirect("home:main")

# Create your views here.
