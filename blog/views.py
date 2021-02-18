from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Rohit',
        'title': 'Blog Post 1',
        'content': 'First Post content',
        'date_posted': 'July 14, 2000',
    },
    {
        'author': 'Salamander',
        'title': 'Blog Post 2',
        'content': 'Second Post content',
        'date_posted': 'July 14, 2000',
    },
    {
        'author': 'Anshu',
        'title': 'Blog Post 3',
        'content': 'Third Post content',
        'date_posted': 'July 14, 2000',
    }
]

context = {'posts': posts}


def home(request):
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
