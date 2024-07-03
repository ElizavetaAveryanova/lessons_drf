from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner
from materials.tasks import send_information_about_update

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для курса
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        Метод получения разрешений
        :return: возвращает список разрешений
        """
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer,
            )
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                IsModer | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer | IsOwner,
            )
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Метод получения владельца курса
        :param serializer: на вход получаем сериализатор
        """
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        subscribed_users = Subscription.objects.filter(course=instance).values_list('user__email', flat=True)

        for user_email in subscribed_users:
            send_information_about_update.delay(
                subject=f"Обновление курса {instance.title}",
                message=f"Курс {instance.title} был обновлен, проверьте на сайте",
                email=user_email
            )

        return instance


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Контроллер создания урока
    """
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )

    def perform_create(self, serializer):
        """
        Метод получения владельца урока
        :param serializer: на вход получаем сериализатор
        """
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    Контроллер получения списка уроков
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        """
        Метод получения уроков с фильтрацией по владельцу
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер просмотра конкретного урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер обновления конкретного урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Контроллер удаления конкретного урока
    """
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModer | IsOwner,
    )


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для работы с подписками
    """

    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )
    queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        """
        Метод создания подписки, если подписка уже есть, то удаляет ее
        :return: Возвращает сообщение об успешной подписке
        """
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})

