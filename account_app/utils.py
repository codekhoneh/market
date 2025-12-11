from django.core.mail import send_mail
from django.conf import settings


def send_email_otp(email, code):
    """
    ارسال کد OTP به ایمیل کاربر
    """
    subject = "کد تایید ثبت‌نام"
    message = f"""
سلام،

کد تایید شما: {code}

این کد برای 10 دقیقه معتبر است.

با تشکر،
تیم پشتیبانی
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(f"✅ ایمیل به {email} ارسال شد")
        return True
    except Exception as e:
        print(f"❌ خطا در ارسال ایمیل: {e}")
        return False
