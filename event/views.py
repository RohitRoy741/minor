from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import event
from users.models import Profile
from django.contrib.auth.models import User


class EventCreateView(CreateView):
    model = event
    fields = ['title', 'date', 'venue', 'club']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
