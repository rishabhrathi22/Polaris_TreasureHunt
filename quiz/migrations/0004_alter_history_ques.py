# Generated by Django 4.0.1 on 2022-01-11 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_rename_riddles_riddle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='ques',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.riddle'),
        ),
    ]
