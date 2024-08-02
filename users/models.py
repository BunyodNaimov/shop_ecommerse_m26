from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import phone_validator


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        blank=True, )
    email = models.EmailField(_("email address"), null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, validators=[phone_validator])
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    billing_address = models.CharField(help_text="Адрес для выставления счета", max_length=256, null=True, blank=True)
    shipping_address = models.CharField(help_text="Адрес доставки", max_length=256, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username
