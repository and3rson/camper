# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 14:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[('sensor', 'Sensor'), ('switch', 'Switch'), ('rotor', 'Rotor')], max_length=32)),
                ('date_last_updated', models.DateTimeField(blank=True, null=True)),
                ('input_channels', models.ManyToManyField(blank=True, related_name='things', to='channels.InputChannel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
