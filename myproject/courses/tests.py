from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )

        self.course = Course.objects.create(
            name='Test Course',
            owner=self.user1
        )

        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            link='https://www.youtube.com/watch?v=test123',
            course=self.course,
            owner=self.user1
        )

        self.lessons_list_url = reverse('lesson-list')
        self.lesson_detail_url = reverse('lesson-detail', args=[self.lesson.id])

    def test_create_lesson_invalid_youtube_link(self):
        """Тест: недопустимая ссылка"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'name': 'New Lesson',
            'link': 'https://www.example.com/video123',
            'course': self.course.id
        }
        response = self.client.post(self.lessons_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('YouTube', str(response.data))

    def test_update_lesson_owner(self):
        """Тест: обновление владельцем"""
        self.client.force_authenticate(user=self.user1)
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(self.lesson_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_not_owner(self):
        """Тест: обновление не владельцем"""
        self.client.force_authenticate(user=self.user2)
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(self.lesson_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )

        self.course = Course.objects.create(
            name='Test Course',
            owner=self.user1
        )

        self.create_url = reverse('subscription-create')
        self.delete_url = reverse('subscription-delete')
        self.course_detail_url = reverse('course-detail', args=[self.course.id])

    def test_create_subscription(self):
        """Тест: создание подписки"""
        self.client.force_authenticate(user=self.user2)
        data = {'course': self.course.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user2, course=self.course).exists())

    def test_create_duplicate_subscription(self):
        """Тест: дубликат подписки"""
        self.client.force_authenticate(user=self.user2)
        Subscription.objects.create(user=self.user2, course=self.course)
        data = {'course': self.course.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_subscription(self):
        """Тест: удаление подписки"""
        self.client.force_authenticate(user=self.user2)
        Subscription.objects.create(user=self.user2, course=self.course)
        data = {'course': self.course.id}
        response = self.client.delete(self.delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_status(self):
        """Тест: статус подписки"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.course_detail_url)
        self.assertFalse(response.data['is_subscribed'])

        Subscription.objects.create(user=self.user2, course=self.course)
        response = self.client.get(self.course_detail_url)
        self.assertTrue(response.data['is_subscribed'])
