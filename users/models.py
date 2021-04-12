from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default="No Bio")
    city = models.CharField(default="Jaipur", max_length=100)
    state = models.CharField(default="Rajasthan", max_length=100)
    programme = models.CharField(default='B.Tech', max_length=15)
    branch = models.CharField(default='CSE', max_length=15)
    face = models.ImageField(blank=True, upload_to='faces')
    face_encode = models.FileField(upload_to='face_encodes', blank=True)
    two_factor = models.BooleanField(default=False)
    following = models.ManyToManyField(
        User, related_name='following')
    follow_request = models.ManyToManyField(
        User, related_name='requests')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
