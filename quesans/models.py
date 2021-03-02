from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Question(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    created_on = models.DateTimeField(auto_now=True)
    slug=models.SlugField()
    #add image
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.desc[:25]+"..."

    def get_absolute_url(self):
        return reverse('quesans:qlist')


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.question.title+'-'+self.user.username

    def get_absolute_url(self):
        #redirect back to question
        return reverse('quesans:qthread',kwargs={'slug':self.question.slug})


class QuestionGroups(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
