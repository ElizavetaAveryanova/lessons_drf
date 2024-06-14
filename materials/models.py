from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials_media/courses/previews",
        verbose_name="Превью",
        **NULLABLE,
        help_text="Загрузите превью курса"
    )
    description = models.TextField(
        verbose_name="Описание курса",
        **NULLABLE,
        help_text="Опишите основные материалы курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )

    title = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(
        verbose_name="Описание урока",
        **NULLABLE,
        help_text="Опишите основные материалы урока"
    )
    preview = models.ImageField(
        upload_to="materials_media/lessons/previews",
        verbose_name="Превью урока",
        **NULLABLE,
        help_text="Загрузите превью урока"
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        **NULLABLE,
        help_text="Укажите ссылку на видео урока"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
