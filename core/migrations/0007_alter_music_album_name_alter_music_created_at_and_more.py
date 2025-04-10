# Generated by Django 5.1.7 on 2025-04-07 15:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_music_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='album_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='genre',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
