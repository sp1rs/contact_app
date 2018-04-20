# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-20 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=31)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('image_url', models.CharField(max_length=63, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(db_index=True, max_length=16, unique=True)),
                ('type', models.CharField(choices=[(b'home', b'home'), (b'office', b'office')], max_length=10)),
                ('code', models.CharField(max_length=5)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='contact_book.Contact')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]