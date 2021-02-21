from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

context = {'posts': Post.objects.all()}


def home(request):
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
