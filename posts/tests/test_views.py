from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from posts.models import Group, Post, User


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Тестовая группа',
            slug='cats',
            description='Текст описания'
        )
        Post.objects.create(
            text='Тестовый пост',
            author=User.objects.create(username='Тестовый автор'),
            group=Group.objects.create(title='Тестовая группа')
        )
        cls.user_1 = User.objects.create_user(username='Alex Morgan')
        cls.group_1 = Group.objects.create(
            id=25,
            title='Когорка 25',
            slug='Backend',
            description='Не придумал'
        )
        cls.group_2 = Group.objects.create(
            id=7,
            title='Когорка 7',
            slug='Full_stack',
            description='Не придумал'
        )
        cls.post_1 = Post.objects.create(
            text='Тестовый пост',
            author=cls.user_1,
            group=cls.group_2
        )

    def setUp(self):
        # Создаем авторизованный клиент
        User = get_user_model()
        self.user = User.objects.create_user(username='Alex_view')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('index'),
            'posts/new_post.html': reverse('new_post'),
            'group.html': reverse('group', kwargs={'slug': 'cats'}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        post_text_0 = response.context.get('posts')[0].text
        post_author_0 = response.context.get('posts')[0].author
        post_group_0 = response.context.get('posts')[0].group
        self.assertEqual(post_text_0, 'Тестовый пост', post_text_0)
        self.assertEqual(post_author_0.username, 'Alex Morgan', post_text_0)
        self.assertEqual(post_group_0.title, 'Когорка 7', post_group_0)

    def test_group_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'group', kwargs={'slug': 'cats'}))
        group_title_0 = response.context.get('group').title
        group_slug_0 = response.context.get('group').slug
        group_description_0 = response.context.get('group').description
        self.assertEqual(group_title_0, 'Тестовая группа', group_title_0)
        self.assertEqual(group_slug_0, 'cats', group_slug_0)
        self.assertEqual(group_description_0,
                         'Текст описания',
                         group_description_0)

    def test_new_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        # Список ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields_new = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields_new.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_user_get_post(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context.get('posts')[0], self.post_1)

    def test_user_get_post(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'Full_stack'}))
        self.assertEqual(response.context.get('posts')[0], self.post_1)

    def test_user_get_post(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'cats'}))
        self.assertNotEqual(response.context.get('posts'), self.post_1)
