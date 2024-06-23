from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
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
        validators = [LinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_list = LessonSerializer(source='lessons', many=True, read_only = True)

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
        )