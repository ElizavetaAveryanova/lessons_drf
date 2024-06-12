from django.urls import path

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("users/create/", UserCreateAPIView.as_view(), name="users_create"),
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>", UserRetrieveAPIView.as_view(), name="users_detail"),
    path("users/update/<int:pk>", UserUpdateAPIView.as_view(), name="users_update"),
    path("users/delete/<int:pk>", UserDestroyAPIView.as_view(), name="users_delete"),
]