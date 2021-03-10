from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from blog.models import Post
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from . import face_id as fi


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class CustomLogin(LoginView):

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            profile = Profile.objects.get(user=user)
            if profile.two_factor:
                if fi.faceLogin(profile.face_encode.url, profile.user.username):
                    return self.form_valid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            instance = p_form.save(commit=False)
            if instance.two_factor == True:
                fi.faceCapture(instance)
                instance.save()
            instance.save()
            messages.success(
                request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def profile_page(request, pk):
    context = {"user": User.objects.get(
        id=pk), 'posts': Post.objects.all()}
    return render(request, "users/profile_page.html", context)
