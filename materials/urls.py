from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView, SubscriptionCreateAPIView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path(
        "lessons/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lessons_update"),
    path(
        "lessons/<int:pk>/delete",
        LessonDestroyAPIView.as_view(),
        name="lessons_destroy",
    ),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create')
]

urlpatterns += router.urls
