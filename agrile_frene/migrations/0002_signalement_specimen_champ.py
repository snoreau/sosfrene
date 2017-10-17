# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 23:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agrile_frene', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signalement',
            name='accepte',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='signalement',
            name='specimen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Specimen'),
        ),
    ]