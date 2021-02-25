from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Тестовый автор')
        cls.group = Group.objects.create(
            title='Когорка 25',
            slug='Backend',
            description='Не придумал'
        )
        cls.group_1 = Group.objects.create(
            title='Когорка 7',
            slug='Full_stack',
            description='Не придумал'
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='Alex Morgan')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/new_post.html': reverse('posts:new_post'),
            'group.html': reverse('posts:group', kwargs={'slug': 'Full_stack'}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context.get('post_list')[0],
                         self.post,
                         'Сообщение об ошибке')

    def test_group_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:group', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.context.get('group'),
                         self.group,
                         'Сообщение об ошибке')

    def test_new_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields_new = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields_new.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_user_get_post(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context.get('posts')[0], self.post)

    def test_user_get_post(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'Full_stack'}))
        self.assertEqual(response.context.get('posts')[0], self.post)

    def test_user_get_post(self):
        response = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': 'cats'}))
        self.assertNotEqual(response.context.get('posts'), self.post)
