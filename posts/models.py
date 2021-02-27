from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Заголовок',
                             max_length=200,
                             help_text='Назовите как-то кгруппу')
    slug = models.SlugField('Введите понятную вам часть URL',
                            unique=True,
                            help_text='Часть Url - это как заголовок, '
                                      'но в адресной строке')
    description = models.TextField('Описание',
                                   max_length=1000,
                                   help_text='расскажите, что происходит '
                                             'в вашей группе )')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст',
                            help_text='основное содержание поста')
    pub_date = models.DateTimeField('Дата',
                                    auto_now_add=True,
                                    help_text='Дата создания Поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Имя автора',
                               help_text='имя автора')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='group',
                              blank=True, null=True,
                              verbose_name='Название группы',
                              help_text='Название группы')

    def __str__(self):
        return self.text[:15]
