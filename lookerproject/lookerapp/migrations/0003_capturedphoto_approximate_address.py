# Generated by Django 5.0.1 on 2024-07-05 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookerapp', '0002_capturedphoto_delete_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='capturedphoto',
            name='approximate_address',
            field=models.TextField(default='Unknown'),
        ),
    ]