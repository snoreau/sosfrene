# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 22:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('type', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DetailSignalement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('contenu', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('activite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Activite')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Signalement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=500)),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Localisation')),
            ],
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(max_length=50)),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Localisation')),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notifications', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='signalement',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Utilisateur'),
        ),
        migrations.AddField(
            model_name='notification',
            name='specimen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Specimen'),
        ),
        migrations.AddField(
            model_name='message',
            name='expediteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='agrile_frene.Utilisateur'),
        ),
        migrations.AddField(
            model_name='message',
            name='receveur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='agrile_frene.Utilisateur'),
        ),
        migrations.AddField(
            model_name='detailsignalement',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Photo'),
        ),
        migrations.AddField(
            model_name='detailsignalement',
            name='signalement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Signalement'),
        ),
        migrations.AddField(
            model_name='activite',
            name='specimen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agrile_frene.Specimen'),
        ),
    ]
