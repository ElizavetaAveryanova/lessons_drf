from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from materials.models import Course, Lesson

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

class Payments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment",)
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="paid_course",
        related_name="paid_course",
        **NULLABLE,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="paid_lesson",
        related_name="paid_lesson",
        **NULLABLE,
    )

    data = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    payment_count = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=50, verbose_name="Метод оплаты")

    def __str__(self):
        return f"{self.user} - {self.paid_course if self.paid_course else self.paid_lesson}"

    def clean(self):
        if self.paid_course is None and self.paid_lesson is None:
            raise ValidationError("Должен быть указан либо курс, либо урок.")
        if self.paid_course is not None and self.paid_lesson is not None:
            raise ValidationError("Нельзя указывать одновременно курс и урок.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"