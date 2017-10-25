# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputChannel',
            fields=[
                ('id', models.SlugField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('json_path', models.CharField(default='$.value', max_length=128)),
                ('data', models.TextField(blank=True, null=True)),
                ('date_last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='channels.InputChannel')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.Value'),
        ),
    ]
