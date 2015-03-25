# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(verbose_name='email', max_length=75, unique=True)),
                ('full_name', models.CharField(verbose_name='name', max_length=30)),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, verbose_name='groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
    ]
