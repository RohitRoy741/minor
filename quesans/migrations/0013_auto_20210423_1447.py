# Generated by Django 3.1.6 on 2021-04-23 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quesans', '0012_auto_20210423_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
    ]
