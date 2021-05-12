from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import event
from users.models import Profile
from django.contrib.auth.models import User
from django import forms


class EventCreateView(CreateView):
    model = event
    fields = ['title', 'date', 'venue', 'club']
    template_name = 'event/create.html'

    def get_form(self, form_class=None):
        form = super(EventCreateView, self).get_form(form_class)
        form.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
