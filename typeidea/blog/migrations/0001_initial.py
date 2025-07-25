# Generated by Django 5.2.4 on 2025-07-17 06:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete')], default=1, verbose_name='status')),
                ('is_nav', models.BooleanField(default=False, verbose_name='is navigation')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete')], default=1, verbose_name='status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('abstract', models.CharField(blank=True, max_length=1024, verbose_name='abstract')),
                ('content', models.TextField(help_text='content must be markdown format.', verbose_name='content')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete'), (2, 'draft')], default=1, verbose_name='status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tag', verbose_name='tag')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'article',
                'ordering': ['-id'],
            },
        ),
    ]
