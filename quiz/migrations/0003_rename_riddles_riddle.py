# Generated by Django 4.0.1 on 2022-01-11 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_riddles'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Riddles',
            new_name='Riddle',
        ),
    ]
