# Generated by Django 3.1.6 on 2021-05-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_profile_face_encode'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
