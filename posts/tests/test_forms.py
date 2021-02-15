from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="test-name")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            description="Группа для тестирования",
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            "text:": "Тестовый текст поста",
            "author": self.user,
            "group": PostFormTests.group.id,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse("new_post"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, "/")
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(group=PostFormTests.group.id).exists()
        )
