from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = None

    email = models.EmailField(
        verbose_name="Почта", unique=True, help_text="Укажите почту"
    )

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=35,
        **NULLABLE,
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        verbose_name="город", max_length=50, **NULLABLE, help_text="Укажите город"
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars",
        **NULLABLE,
        help_text="Аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email
