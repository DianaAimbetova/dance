# Generated by Django 4.2.2 on 2023-07-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0003_alter_class_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='video_url',
            field=models.URLField(blank=True),
        ),
    ]