# Generated by Django 2.2.9 on 2021-02-25 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210211_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Часть Url - это как заголовок, но в адресной строке', unique=True, verbose_name='Введите понятную вам часть URL'),
        ),
    ]
