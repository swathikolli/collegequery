# Generated by Django 3.2 on 2021-05-08 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0002_rename_user_person'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Person',
            new_name='User',
        ),
    ]