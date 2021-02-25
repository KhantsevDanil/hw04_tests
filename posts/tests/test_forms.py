from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    group = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Alex_Morgan')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Описание тестовой группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'group': PostCreateFormTests.group.id,
            'text': 'Тестовый пост',
        }
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        test_group = Post.objects.get(id=posts_count)
        self.assertEqual(test_group.text, 'Тестовый пост')

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Измененный пост',
            'group': self.group.id,
        }
        test_post = Post.objects.create(
            text='Тестовый пост',
            author=self.user,
        )
        kwargs = {'username': self.user.username, 'post_id': test_post.id}
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs=kwargs),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse('posts:post_view', kwargs=kwargs))
