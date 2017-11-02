# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 14:50
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('thing:change', 'Thing changed'), ('value:change', 'Value changed')], max_length=32)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('object_id', models.SlugField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('object_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
