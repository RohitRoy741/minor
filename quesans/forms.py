from django import forms
from . import models
from tinymce import TinyMCE

class PostQues(forms.ModelForm):
    desc = forms.CharField(widget=TinyMCE(mce_attrs={'width': 500}))
    class Meta:
        model = models.Question
        fields =['title','desc','image']

class PostAns(forms.ModelForm):
    answer_text = forms.CharField(widget=TinyMCE(mce_attrs={'width':800}))
    class Meta:
        model = models.Answer
        fields = ['answer_text','is_anonymous']

class PostReply(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ['body']
    def __init__(self, *args, **kwargs):
        super(PostReply, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'placeholder': 'Reply here...', 'class':'form-control', 'rows':'5'}
