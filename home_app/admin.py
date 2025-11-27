from django.contrib import admin
from django import forms 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from account_app.models import User

class UserCreationForm(forms.ModelForm): 
    """ساخت فرم کاربر جدید در پنل ادمین """ 
    password1 = forms.CharField(label='گذروتژه', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='تکرار گذرواژه ', widget=forms.PasswordInput) 
 
    class Meta: 
        model = User 
        fields = ('phone', 'email', 'full_name') 
 
    def clean_password2(self): 
        password1 = self.cleaned_data.get("password1") 
        password2 = self.cleaned_data.get("password2") 
        if password1 and password2 and password1 != password2: 
            raise forms.ValidationError(" گذر واژه ها یکسان نیستند ") 
        return password2 
    
    def save(self, commit=True): 
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data["password1"]) 
        if commit: 
            user.save() 
        return user 
 
class UserChangeForm(forms.ModelForm): 
    """ فرم ویرایش کاربر در پنل ادمین""" 
    password = ReadOnlyPasswordHashField() 
 
    class Meta: 
        model = User 
        fields = ('phone', 'email', 'full_name', 'password', 'is_active', 'is_admin') 
 
    def clean_password(self): 
        return self.instance.password 
 
class UserAdmin(BaseUserAdmin): 
    # استفاده از فرم های سفارشی  
    form = UserChangeForm 
    add_form = UserCreationForm 
 
    list_display = ('phone', 'email', 'full_name', 'is_admin', 'is_active') 
    list_filter = ('is_admin', 'is_active') 
    fieldsets = ( 
        (None, {'fields': ('phone', 'password')}), 
        ('اطلاعات شخصی', {'fields': ('full_name', 'email')}), 
        (' نوع دسترسی ', {'fields': ('is_admin', 'is_active')}), 
        (' تاریخ های مهم ', {'fields': ('last_login',)}), 
    ) 
    add_fieldsets = ( 
        (None, { 
            'classes': ('wide',), 
            'fields': ('phone', 'email', 'full_name', 'password1', 'password2'), 
        }), 
    ) 
    search_fields = ('phone', 'email', 'full_name') 
    ordering = ('phone',) 
    filter_horizontal = () 
 
admin.site.register(User, UserAdmin)