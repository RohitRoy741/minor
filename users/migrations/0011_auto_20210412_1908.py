# Generated by Django 3.1.6 on 2021-04-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_profile_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='branch',
            field=models.CharField(default='CSE', max_length=15),
        ),
        migrations.AddField(
            model_name='profile',
            name='programme',
            field=models.CharField(default='B.Tech', max_length=15),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Jaipur', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(default='Rajasthan', max_length=100),
        ),
    ]
