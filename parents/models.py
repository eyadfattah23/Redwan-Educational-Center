from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import phonenumbers


class ParentManager(BaseUserManager):
    '''Custom manager for the Parent model to handle user creation and normalization.'''

    def create_user(self, phone_whatsapp, password=None, **extra_fields):
        if not phone_whatsapp:
            raise ValueError('The WhatsApp phone number must be provided.')

        phone_whatsapp = self.normalize_phone(phone_whatsapp)
        extra_fields.setdefault('is_active', True)

        user = self.model(phone_whatsapp=phone_whatsapp, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_whatsapp, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_whatsapp, password, **extra_fields)

    def normalize_phone(self, phone):
        try:
            parsed = phonenumbers.parse(phone, "EG")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except:
            return phone


class Parent(AbstractBaseUser, PermissionsMixin):
    '''Parent model representing a guardian or parent in the system.'''
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_whatsapp = models.CharField(max_length=20, unique=True)
    phone_alt = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)  # internal admin notes

    USERNAME_FIELD = 'phone_whatsapp'
    REQUIRED_FIELDS = ['full_name']

    objects = ParentManager()

    def __str__(self):
        return f"{self.full_name} ({self.phone_whatsapp})"
