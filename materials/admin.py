from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "preview", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "description", "preview", "video_link")


@admin.register(Subscription)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "created_at")
