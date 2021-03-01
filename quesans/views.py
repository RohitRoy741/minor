from django.shortcuts import render,redirect
from .models import Question,Answer,QuestionGroups
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import forms
from .models import Question,Answer
from django.urls import reverse

class QuestionListView(ListView):
    model=Question
    template_name='quesans/listall.html'
    context_object_name='questions'
    ordering=['created_on']

class YourQuestionListView(LoginRequiredMixin,ListView):
    model=Question
    template_name='quesans/listall.html'
    context_object_name='questions'
    ordering=['created_on']

    def get_queryset(self):
        questions=Question.objects.all().filter(author=self.request.user)
        return questions

class PostQuestionView(LoginRequiredMixin,CreateView):
    model = Question
    fields=['title','desc']
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Question
    fields=['title','desc']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

    def get_absolute_url(self):
        return reverse('quesans:qlist')

class QuestionAnswerView(DetailView):
    model = Question
    context_object_name='question'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        return Question.objects.get(slug=self.kwargs.get("slug"))

    def get_context_data(self,**kwargs):
        object=self.get_object()
        context=super().get_context_data(**kwargs)
        try:
            context['answers'] = Answer.objects.all().filter(question=object)
            return context
        except:return None

class AnswerPostView(LoginRequiredMixin,CreateView):
    model = Answer
    fields=['answer_text']

    def get_context_data(self, **kwargs):
        kwargs['question'] = Question.objects.get(pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.question=Question.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class AnswerDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Answer
    success_url = '/quesans'
    
    def test_func(self):
        answer = self.get_object()
        if self.request.user==answer.user:
            return True
        else:return False
