# Generated by Django 5.0.1 on 2024-07-05 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookerapp', '0004_remove_capturedphoto_approximate_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='capturedphoto',
            name='address',
            field=models.TextField(default=False),
        ),
    ]
