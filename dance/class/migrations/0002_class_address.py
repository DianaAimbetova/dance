# Generated by Django 4.2.2 on 2023-07-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='address',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
