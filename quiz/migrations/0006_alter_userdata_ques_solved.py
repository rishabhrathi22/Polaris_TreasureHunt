# Generated by Django 4.0.1 on 2022-01-17 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_remove_riddle_riddle_riddle_correct_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='ques_solved',
            field=models.IntegerField(default=0),
        ),
    ]
