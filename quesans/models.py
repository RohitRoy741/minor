from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from tinymce import HTMLField

class Question(models.Model):
    title = models.CharField(max_length=100)
    desc = HTMLField('desc')
    #models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    created_on = models.DateTimeField(auto_now=True)
    #image = models.ImageField(null=True,blank=True,upload_to ='ques_images/')
    qupvote = models.ManyToManyField(User,related_name = 'q_upvote')
    qdownvote = models.ManyToManyField(User,related_name = 'q_downvote')
    bookmarked = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    slug=models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.desc[:25]+"..."

    def get_absolute_url(self):
        return reverse('quesans:qthread',kwargs={'slug':self.slug})


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = HTMLField('content')
    #models.TextField()
    date = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    upvote = models.ManyToManyField(User,related_name = 'upvote')
    downvote = models.ManyToManyField(User,related_name = 'downvote')
    #image = models.ImageField(null=True,blank=True,upload_to ='ans_images/')

    def __str__(self):
        return self.question.title+'-'+self.user.username

    def get_absolute_url(self):
        #redirect back to question
        return reverse('quesans:qthread',kwargs={'slug':self.question.slug})

    def get_replies(self):
        return self.replies.filter(parent=None).filter(active=True)

class Reply(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE, related_name="replies")
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    def get_replies(self):
        return Reply.objects.filter(parent=self).filter(active=True)
