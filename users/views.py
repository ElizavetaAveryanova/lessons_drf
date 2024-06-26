from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Контроллер регистрации пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """
    Контроллер получения списка пользователей.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер получения информации о конкретном пользователе.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер обновления информации о конкретном пользователе.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Контроллер удаления информации о конкретном пользователе.
    """

    queryset = User.objects.all()


class PaymentListAPIView(generics.ListCreateAPIView):
    """
    Контроллер получения списка платежей пользователя.
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "payment_method",
        "paid_course",
        "paid_lesson",
    )
    ordering_fields = ("data",)

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentCreateAPIView(CreateAPIView):
    """
    Контроллер создания платежа
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер получения информации о конкретном платеже.
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)
