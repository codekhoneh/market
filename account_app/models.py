from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin,
)


class UserManager(BaseUserManager):
	def create_user(self, phone, password=None, **extra_fields):
		if not phone:
			raise ValueError("Users must have a phone number")
		user = self.model(phone=phone, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone, password=None, **extra_fields):
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_admin') is not True:
			raise ValueError('Superuser must have is_admin=True.')
		return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	phone = models.CharField(max_length=20, unique=True)
	email = models.EmailField(blank=True, null=True)
	full_name = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True)

	objects = UserManager()

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.phone or ''

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'
