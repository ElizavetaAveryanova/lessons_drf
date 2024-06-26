from rest_framework import serializers

from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор платежей пользователя.
    """

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей.
    """

    payments_history = PaymentSerializer(many=True, source="payment", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
