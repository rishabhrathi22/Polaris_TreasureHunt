# Generated by Django 4.0.1 on 2022-01-22 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0006_alter_userdata_ques_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='riddle',
            name='hint',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='HintData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.riddle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
