from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from users.models import Profile
from django.contrib.auth.models import User
from event.models import event


def home(request):
    return render(request, 'blog/home.html')


class SearchView(ListView):
    model = User
    template_name = 'blog/base.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = User.objects.filter(username__contains=query)
            result = postresult
        else:
            result = None
        return result

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["liked"] = liked
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def notification(request, pk):
    return render(request, 'blog/notification.html')


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        lst = []
        for likes in self.request.user.post_likes.all():
            lst.append(likes.id)
        context['lst'] = lst
        events = event.objects.all()
        liked_events = []
        for ev in self.request.user.interested.all():
            liked_events.append(ev.id)
        context['events'] = events
        context['interested'] = liked_events
        return context


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    data = {
        'value': liked,
        'count': post.likes.count()
    }
    return JsonResponse(data, safe=False)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def DevelopmentView(request):
    return render(request, 'blog/DevelopmentTeam.html')


class EventListView(ListView):
    model = event
    template_name = 'blog/base.html'
    context_object_name = 'events'
    ordering = ['-date_posted']
