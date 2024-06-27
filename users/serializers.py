from rest_framework import serializers

from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор платежей пользователя.
    """

    class Meta:
        model = Payments
        exclude = (
            "tokens",
            "payment_id",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей.
    """

    payments_history = PaymentSerializer(many=True, source="payment", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "first_name",
            "last_name",
            "is_active",
            "payments_history",
            "last_login",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля"""

    class Meta:
        model = User
        fields = '__all__'
