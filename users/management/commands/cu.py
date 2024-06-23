from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда создания нового пользователя."""

    def handle(self, *args, **options):
        user_email = input("Введите email пользователя: ")
        if User.objects.filter(email=user_email).exists():
            print("Пользователь с таким email уже существует.")
        else:
            user = User.objects.create(email=user_email)
            user.save()
            print(f"Пользователь {user_email} успешно создан.")
