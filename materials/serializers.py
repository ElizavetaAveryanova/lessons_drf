from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для урока
    """
    class Meta:
        model = Lesson
        fields = (
            "id",
            "course",
            "title",
            "description",
            "owner",
            "video_link",
        )
        validators = [LinkValidator(field="video_link")]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курса
    """
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    lessons_list = LessonSerializer(source="lessons", many=True, read_only=True)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context["request"].user, course=obj
        ).exists()

    @staticmethod
    def get_lessons_count(obj: Course) -> int:
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_count",
            "lessons_list",
            "owner",
            "is_subscribed",
        )
