from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Payment
from users.serializers import PaymentSerializer, UserSerializer
from rest_framework import generics


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
