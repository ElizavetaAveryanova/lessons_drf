from django.core.management import BaseCommand
from materials.models import Lesson, Course


class Command(BaseCommand):
    """Команда создания нового пользователя."""

    def handle(self, *args, **options):
        course_id = int(input("Введите id курса: "))
        if not Course.objects.filter(id=course_id).exists():
            print("Курс с таким id не найден.")

        lesson_title = input("Введите название урока: ")
        lesson_description = input("Введите описание урока: ")

        if course_id is not None:
            lesson = Lesson.objects.create(
                course_id=course_id, title=lesson_title, description=lesson_description
            )
            print("Урок успешно создан.")
            lesson.save()
        else:
            print("Не удалось создать урок.")
