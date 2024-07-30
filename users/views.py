from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Payment
from users.serializers import PaymentSerializer, UserSerializer
from rest_framework import generics

from users.services import create_stripe_price, create_stripe_session


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_type')
    ordering_fields = ('datetime_payment',)


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Создаем новую оплату, с владельцем, текущим, авторизованным пользователем
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(owner=self.request.user)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('paid_lesson'):
            lesson = serializer.validated_data.get('paid_lesson')
            price = lesson.price
            price_stripe = create_stripe_price(price, lesson.title)
        elif serializer.validated_data.get('paid_course'):
            course = serializer.validated_data.get('paid_course')
            price = sum(lesson.price for lesson in course.lesson.all())
            price_stripe = create_stripe_price(price, course.title)
        else:
            raise ValueError("Не указан paid_lesson или paid_course")
        payment.price = price
        session_id, link = create_stripe_session(price_stripe)
        payment.session_id = session_id
        payment.link = link
        payment.save()



class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
