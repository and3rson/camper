# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 21:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('values', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='RangeControl',
            fields=[
                ('control_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='controls.Control')),
                ('min_value', models.FloatField()),
                ('max_value', models.FloatField()),
                ('step', models.FloatField()),
                ('is_float', models.BooleanField(default=True)),
            ],
            bases=('controls.control',),
        ),
        migrations.CreateModel(
            name='SwitchControl',
            fields=[
                ('control_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='controls.Control')),
                ('is_enabled', models.BooleanField(default=False)),
            ],
            bases=('controls.control',),
        ),
        migrations.AddField(
            model_name='control',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='control',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='values.Value'),
        ),
    ]
