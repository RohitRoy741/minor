from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


class event(models.Model):
    creator = models.ForeignKey(
        User, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateField()
    venue = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    interested = models.ManyToManyField(User, related_name='interested')

    def get_absolute_url(self):
        return reverse('blog-home')
