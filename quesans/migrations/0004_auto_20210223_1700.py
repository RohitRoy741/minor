# Generated by Django 3.1.6 on 2021-02-23 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quesans', '0003_question_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='updated_on',
        ),
        migrations.AddField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
