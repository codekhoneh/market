from django import forms 
from django.contrib import admin 
from django.contrib.auth.models import Group 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from django.core.exceptions import ValidationError 
from django.core.validators import RegexValidator
from account_app.models import User
from django.core import validators

def fa_to_en_digits(s):
    """تبدیل اعداد فارسی به انگلیسی"""
    mapping = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    return s.translate(mapping)
def validate_password_strength(password): 
    """ 
    بررسی قانون رمز عبور:
    - حداقل ۸ کاراکتر
    - شامل حرف بزرگ
    - شامل حرف کوچک
    - شامل عدد
    - شامل کاراکتر خاص
    """ 
    if len(password) < 8: 
        raise ValidationError("رمز عبور حداقل شامل ۸ کاراکتر باشد") 
     
    if not any(c.isupper() for c in password): 
        raise ValidationError("رمز عبور باید شامل حرف بزرگ باشد") 
     
    if not any(c.islower() for c in password): 
        raise ValidationError("رمز عبور باید شامل حرف کوچک باشد") 
     
    if not any(c.isdigit() for c in password): 
        raise ValidationError("رمز عبور باید شامل عدد باشد") 
     
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?" 
    if not any(c in special_chars for c in password): 
        raise ValidationError("رمز عبور باید شامل کاراکتر خاص باشد(!@#$%^&*و غیره)")
phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message='شماره تلفن باید با 09 شروع شود و 11 رقم باشد',
) 
 
class RegisterForm(forms.Form): 
    phone = forms.CharField( 
        max_length=11, 
        validators=[phone_validator], 
        label="شماره تلفن", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "مثال: 09301234567"}),
    )
    
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمز عبور خود را وارد کنید"}),
    )
    email = forms.EmailField( 
        required=False, 
        label="ایمیل", 
        widget=forms.EmailInput(attrs={ 
            "class": "form-control", 
            "placeholder": "مثال: user@example.com" 
        })
    )
    def clean(self): 
        cleaned = super().clean() 
        phone = cleaned.get("phone") 
        email = cleaned.get("email") 
        if not phone and not email: 
            raise ValidationError("وارد کردن شماره تلفن یا ایمیل الزامی است") 
        return cleaned 
    def clean_phone(self): 
        phone = self.cleaned_data.get('phone', '') 
        phone = fa_to_en_digits(phone) 
        phone = ''.join(phone.split())     
        phone = phone.replace('-', '')      
        return phone
class CheckOTPForm(forms.Form): 
    code = forms.CharField( 
    max_length=4, 
    validators=[RegexValidator(regex=r'^\d{4}$', message=" کد باید شامل 4 رقم باشد")], 
    label="کد امنیتی", 
    widget=forms.TextInput(attrs={"placeholder": "کد ارسال شده را وارد کنید"}))

class UserCreationForm(forms.ModelForm): 
    password1 = forms.CharField(label='گذر واژه', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='تکرار گذر واژه', widget=forms.PasswordInput) 
 
    class Meta: 
        model = User 
        fields = ('phone', 'full_name', 'email') 

    def clean_password2(self): 
        password1 = self.cleaned_data.get("password1") 
        password2 = self.cleaned_data.get("password2") 
        if password1 and password2 and password1 != password2: 
            raise ValidationError("گذر واژه ها یکسان نیستند") 
        return password2
    
    def save(self, commit=True): 
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data["password1"]) 
        if commit: 
            user.save() 
        return user
# -------------------------------------------------------------------------------------    
class UserChangeForm(forms.ModelForm): 
    password = ReadOnlyPasswordHashField() 
        
    class Meta: 
        model = User 
        fields = ('phone', 'full_name', 'email', 'password', 'is_active', 'is_admin') 

    def clean_password(self): 
        return self.instance.password
# ------------------------------------------------------------------------------------
class LoginForm(forms.Form): 
    identifier = forms.CharField( 
        label="ایمیل یا شماره تلفن", 
        widget=forms.TextInput(attrs={ 
            'class': 'form-control identifier-field', 
            'placeholder': 'ایمیل یا شماره تلفن خود را وارد کنید' 
        }))
    password = forms.CharField( 
        label="رمز عبور", 
        widget=forms.PasswordInput(attrs={ 
            'class': 'form-control password-field', 
            'placeholder': 'رمز عبور خود را وارد کنید'}), strip=False)
    
    def clean_identifier(self): 
        ident = self.cleaned_data.get('identifier', '').strip() 
        ident = fa_to_en_digits(ident).replace('-', '').replace(' ', '')
        return ident