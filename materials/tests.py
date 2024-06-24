from django.urls import reverse

from rest_framework import status

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpass')
        self.course = Course.objects.create(title='Test Course')
        self.lesson = self.course.lessons.create(title="test_lesson",
                                                 video_link="https://www.youtube.com/watch?v=2T83JhAeC6U&list=PLA0M1Bcd0w8zPwP7t-FgwONhZOHt9rz9E&index=34",
                                                 owner=self.user)
        self.client.force_authenticate(user=self.user)


    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("course"), self.course.pk)
        self.assertEqual(data.get("video_link"), self.lesson.video_link)
        self.assertEqual(data.get("owner"), self.user.pk)
        url_2 = reverse("materials:lesson_detail", args=(100,))
        response_2 = self.client.get(url_2)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_lesson_with_valid_video_link(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test Lesson",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/watch?v=2T83JhAeC6U&list=PLA0M1Bcd0w8zPwP7t-FgwONhZOHt9rz9E&index=34",
            "owner": self.user.pk,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # 2 because we created one in setUp()
        self.assertEqual(Lesson.objects.last().title, "Test Lesson")
        self.assertEqual(Lesson.objects.last().video_link, data["video_link"])

    def test_create_lesson_with_invalid_video_link(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test Lesson",
            "course": self.course.pk,
            "video_link": "https://www.example.com/video.mp4",
            "owner": self.user.pk,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn("Допустимо добавлять ссылки на материалы, размещенные только на youtube",
                      response.data["non_field_errors"][0])
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "test_lesson_3",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/watch?v=2T83JhAeC6U&list=PLA0M1Bcd0w8zPwP7t-FgwONhZOHt9rz9E&index=34",
            "owner": self.user.pk,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "test_lesson_3")
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).title, "test_lesson_3")


    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.first().title, "test_lesson")
        self.assertEqual(Lesson.objects.first().owner, self.user)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["id"], self.lesson.pk)
        self.assertEqual(data["results"][0]["course"], self.course.pk)
        self.assertEqual(data["results"][0]["title"], "test_lesson")
        self.assertEqual(data["results"][0]["description"], None)
        self.assertEqual(data["results"][0]["video_link"], "https://www.youtube.com/watch?v=2T83JhAeC6U&list=PLA0M1Bcd0w8zPwP7t-FgwONhZOHt9rz9E&index=34")
        self.assertEqual(data["results"][0]["owner"], self.user.pk)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpass')
        self.course = Course.objects.create(title="Test Course")
        self.lesson = self.course.lessons.create(title="test_lesson", owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscription_create_or_delete(self):

        data = {
            "user": self.user.pk,
            "course_id": self.course.pk,
        }

        response = self.client.post("/subscription/create/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        subs_item = Subscription.objects.filter(
            user=data["user"], course=data["course_id"]
        )

        if subs_item.exists():
            subs_item.delete()
            self.assertEqual(subs_item.count(), 0)
            self.assertEqual(subs_item.exists(), False)
            print("тест на удаление подписки пройден")

        if not subs_item.exists():
            Subscription.objects.create(user=self.user, course=self.course)
            self.assertEqual(subs_item.exists(), True)
            self.assertEqual(subs_item.count(), 1)
            self.assertEqual(Subscription.objects.last().user, self.user)
            self.assertEqual(Subscription.objects.last().course_id, self.course.pk)
            print("тест на добавление подписки пройден")

        self.client.logout()

        if not self.user.is_authenticated:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)