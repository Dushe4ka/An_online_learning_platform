from django.urls import path
from rest_framework.routers import DefaultRouter

# from .views import MyTokenObtainPairView
from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [

] + router.urls
