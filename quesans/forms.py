from django import forms
from . import models

class PostQues(forms.ModelForm):
    class Meta:
        model = models.Question
        fields =['title','desc']
class PostAns(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['answer_text','is_anonymous']
