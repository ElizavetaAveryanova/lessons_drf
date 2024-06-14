from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"materials", CourseViewSet, basename="course")

urlpatterns = [
    path("materials/lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("materials/lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("materials/lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("materials/lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("materials/lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
] + router.urls




