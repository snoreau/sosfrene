# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agrile_frene', '0005_message_sujet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activite',
            name='specimen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activites', to='agrile_frene.Specimen'),
        ),
        migrations.AlterField(
            model_name='signalement',
            name='specimen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signalement', to='agrile_frene.Specimen'),
        ),
    ]