from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='blog_images/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liking_user', null=True)
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    @classmethod
    def like(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)

    @classmethod
    def dislike(cls, post, disliking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(disliking_user)

    def __str__(self):
        return str(self.post)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
