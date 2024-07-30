from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

