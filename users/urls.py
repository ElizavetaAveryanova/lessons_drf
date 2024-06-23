from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
)

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    # users
    path("users/register/", UserCreateAPIView.as_view(), name="users_register"),
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_detail"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="users_update"),
    path("users/delete/<int:pk>/", UserDestroyAPIView.as_view(), name="users_delete"),
    # payments
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_detail"),
    # path("payment/update/<int:pk>/", PaymentUpdateAPIView.as_view(), name="payment_update"),
    # path(
    #     "payment/delete/<int:pk>/", PaymentDestroyAPIView.as_view(), name="payment_delete"
    # ),
    # token
    path(
        "users/login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "users/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
