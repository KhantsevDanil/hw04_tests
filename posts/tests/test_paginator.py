from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        cls.group = Group.objects.create(
            title='Test',
            description='Много букв'
        )
        posts = [Post(author=cls.user,
                      group=cls.group,
                      text=str(i)) for i in range(13)]
        Post.objects.bulk_create(posts)
        for i in range(0, 12):
            posts.append({
                'author': cls.user,
                'text': i,
                'group': cls.group
            })

    def test_first_page_containse_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)
