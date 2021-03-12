from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default="No Bio")
    face_encode = models.FileField(upload_to='face_encodes', blank=True)
    two_factor = models.BooleanField(default=False)
    following = models.ManyToManyField(
        User, related_name='following')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
