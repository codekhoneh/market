from django import forms 
from django.contrib import admin 
from django.contrib.auth.models import Group 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from django.core.exceptions import ValidationError 
from account_app.models import User

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