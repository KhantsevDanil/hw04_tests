from django.test import TestCase
from posts.models import Group, Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        cls.author = User.objects.create(
            usernam='somethingUser'
        )
        cls.group = Group.objects.create(
            title='f' * 15,
            description='Очень хорошая группа',
            slug='some_slug'
        )
        cls.post = Post.objects.create(
            text='Самый лучший текст',
            pub_date='21.04.2003',
            group=cls.group,
            author=cls.author
        )

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verbose = {
            'text': 'Текст',
            'pub_date': 'Дата',
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name, expected)

    def test_group_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verbose = {
            'title': 'Заголовок',
            'description': 'Описание',
            'slug': 'Введите понятную вам часть URL'
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).verbose_name, expected)

    def test_group_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        field_verbose = {
            'title': 'Назовите как-то кгруппу',
            'description': 'расскажите, что происходит в вашей группе )',
            'slug': 'Часть Url - это как заголовок, но в адресной строке'
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).help_text, expected)

    def test_post_help_text(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verbose = {
            'text': 'основное содержание поста',
            'pub_date': 'Дата создания Поста',
            'author': 'имя автора',
            'group': 'Название группы',
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).help_text, expected)

    def test_text_convert_to_slug(self):
        """save преобразует в slug содержимое поля title."""
        slug = self.group.slug
        self.assertEquals(slug, 'some_slug')

    def test_text_post_text(self):
        """save преобразует в slug содержимое поля title."""
        text = self.post.text
        self.assertEquals(text, 'Самый лучший текст')
