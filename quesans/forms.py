from django import forms
from . import models

class PostQues(forms.ModelForm):
    class Meta:
        model = models.Question
        fields =['title','desc','image']

class PostAns(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['answer_text','is_anonymous','image']

class PostReply(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ['body']
    def __init__(self, *args, **kwargs):
        super(PostReply, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'placeholder': 'Reply here...', 'class':'form-control', 'rows':'5'}
