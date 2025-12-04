from django.db import models 
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
from django.core.validators import RegexValidator 
from django.utils import timezone
from datetime import timedelta
class OTP(models.Model): 
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن") 
    code = models.CharField(max_length=4, verbose_name="کد تایید") 
    token = models.CharField(max_length=255, null=True, blank=True, verbose_name="توکن") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد") 
    def is_expired(self): 
        return timezone.now() > self.created_at + timedelta(minutes=1) 
    def __str__(self): 
        return f"{self.phone} - {self.code}"

class UserManager(BaseUserManager): 
   def create_user(self, phone, full_name, password=None,email=None):
        if not phone: 
            raise ValueError("داشتن شماره تماس الزامی است ") 
 
        user = self.model(phone=phone, full_name=full_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user 
   
   def create_superuser(self, phone, full_name, password=None, email=None): 
        user = self.create_user(phone=phone,full_name=full_name,password=password,email=email) 
        user.is_admin = True 
        user.is_superuser = True 
        user.save(using=self._db) 
        return user
class User(AbstractBaseUser):
    email = models.EmailField(unique=True,blank=True,null=True,max_length=255,verbose_name='ادرس ایمیل') 
    full_name = models.CharField(max_length=200,verbose_name='یربراک مان') 
    phone = models.CharField(max_length=11,unique=True,verbose_name='تلفن',default='00000000000') 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False,verbose_name='ادمین') 

    USERNAME_FIELD ='phone' 
    REQUIRED_FIELDS = ['full_name']   
    objects = UserManager()   
    class Meta: 
        verbose_name='کاربر' 
        verbose_name_plural='کاربرها' 
    def __str__(self): 
      return self.phone or self.email or ""
       
    def has_perm(self, perm, obj=None): 
        return self.is_admin
     
    def has_module_perms(self, app_label): 
        return self.is_admin
    
    @property 
    def is_staff(self): 
        return self.is_admin


