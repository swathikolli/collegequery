# Generated by Django 3.2 on 2021-06-12 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0009_auto_20210512_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='persons_images'),
        ),
    ]
