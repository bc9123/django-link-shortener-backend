# Generated by Django 5.1.7 on 2025-04-02 14:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_remove_shortenedurl_created_at_shortenedurl_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortenedurl',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
