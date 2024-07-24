from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Course Test")
        self.lesson = Lesson.objects.create(name="Test Lesson",
                                            course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        self.data = {
            'name': 'Test Lesson',
            'course': self.course.id
        }
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], self.lesson.name)
        self.assertEqual(data['course'], self.course.id)

    def test_lesson_create(self):
        self.url = reverse("materials:lessons_create")
        self.data = {
            'name': 'New Test Lesson',
            'course': self.course.id,
            'description': 'Test description'
        }
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course'], self.lesson.course.id)
        self.assertEqual(
            Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        self.url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        self.data = {
            'name': 'Updated Test Lesson',
            'course': self.course.id,
            'description': 'Updated Test Description'
        }
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.data['name'])
        self.assertEqual(response.data['description'], self.data['description'])

    def test_lesson_delete(self):
        self.url = reverse("materials:lessons_destroy", args=(self.lesson.pk,))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        self.url = reverse("materials:lessons_list")
        response = self.client.get(self.url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.id,
                    'name': self.lesson.name,
                    'description': None,
                    'preview': None,
                    'video_link': None,
                    'course': self.lesson.course.id,
                    'owner': self.lesson.owner.id
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)



class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@sky.pro")
        self.course = Course.objects.create(name="Course Test")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("materials:subscription_create")

    def test_subscription_activate(self):
        """ Тест подписки на курс """
        data = {
            'user': self.user.id,
            'course': self.course.id
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'message': 'Подписка добавлена'
            }
        )
        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_deactivate(self):
        """ Тест отписки с курса """
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            'user': self.user.id,
            'course': self.course.id
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'message': 'Подписка удалена'
            }
        )
        self.assertFalse(
            Subscription.objects.all().exists()
        )
