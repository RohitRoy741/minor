from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from blog.models import Post
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from . import face_id as fi
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created! Update your profile for better experience.')
            new_user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('profile')
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
                request.session['username'] = username
                request.session['password'] = password
                return redirect('twofactorauth')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def TwoFactorAuth(request):
    return render(request, 'users/facelogin.html')


def postFaceLogin(request):
    username = request.session.get('username')
    password = request.session.get('password')
    user = authenticate(request, username=username, password=password)
    if request.method == 'POST':
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        import base64
        from django.core.files.base import ContentFile
        format, imgstr = post_data['imageString'].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        file_name = user.username+'.'+ext
        user.profile.face.save(file_name, data, save=True)
        if fi.faceLogin(user):
            print('Face login successful')
            user.profile.face.delete(save=True)
            login(request, user)
            return HttpResponseRedirect(reverse('blog-home'))
        user.profile.face.delete(save=True)
        print('facelogin unsuccessful')
        messages.error(
            request, 'Face could not be encoded! Make sure your face is visible')
    return HttpResponseRedirect(reverse('login'))


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(
                request, f'Your account has been updated!')
            instance = p_form.save(commit=True)
            if instance.two_factor == True:
                return redirect('webcam')
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


def follow(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    if profile.following.filter(id=request.user.id).exists():
        profile.following.remove(request.user)
    elif profile.follow_request.filter(id=request.user.id).exists():
        profile.follow_request.remove(request.user)
    else:
        profile.follow_request.add(request.user)
    return HttpResponseRedirect(reverse('suggestions'))


# def follow_request(request, pk):
#     profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
#     if profile.follow_request.filter(id=request.user.id).exists():
#         profile.follow_request.remove(request.user)
#     else:
#         profile.follow_request.add(request.user)
#     return HttpResponseRedirect(reverse('suggestions'))


def accept_follow_request(request, pk):
    profile = request.user.profile
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    print(user.pk)
    profile.following.add(user)
    profile.follow_request.remove(user)
    return HttpResponseRedirect(reverse('suggestions'))


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'users/suggestions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        request_lst = []
        lst = []
        for profile in self.request.user.following.all():
            lst.append(profile.id)
        for profile in self.request.user.requests.all():
            request_lst.append(profile.id)
        context['lst'] = lst
        context['request_lst'] = request_lst
        return context


class vertex():
    def __init__(self, profile, index):
        self.profile = profile
        self.color = 'WHITE'
        self.parent = None
        self.distance = 20000
        self.index = index


class profileGraph():
    def __init__(self, lst):
        self.V = list()
        i = 0
        for profile in lst:
            v = vertex(profile, i)
            i = i+1
            self.V.append(v)
        self.AdjList = list()
        for v1 in self.V:
            lst = list()
            for v2 in self.V:
                if v1.profile.user.following.filter(id=v2.profile.id).exists():
                    lst.append(v2)
            self.AdjList.append(lst)

    def profiles_data(self):
        for v in self.V:
            print(v.profile.user.id)


def bfs(g, source, temp):
    g.V[source].distance = 0
    g.V[source].color = 'GRAY'
    queue = list()
    queue.append(g.V[source])
    while len(queue) > 0:
        u = queue.pop(0)
        for v in g.AdjList[u.index]:
            if v.color == 'WHITE':
                v.color = 'GRAY'
                v.parent = u
                v.distance = u.distance + 1
                queue.append(v)
        u.color = 'BLACK'
        temp.append(u)


def findFriend(request):
    profiles = Profile.objects.all()
    g = profileGraph(profiles)
    g.profiles_data()
    place = None
    x = request.user.profile.id
    for i in range(len(g.V)):
        if g.V[i].profile.id == x:
            place = i
            break
    print(place)
    for lst in g.AdjList:
        for v in lst:
            print(v.profile.user.id, end=' ')
        print()
    temp = list()
    bfs(g, place, temp)
    for v in g.V:
        print(v.profile.user.username, v.distance)
    result = list()
    lst = list()
    request_lst = list()
    for vertex in temp:
        if vertex.parent is None:
            pass
        else:
            if vertex.distance <= 1:
                lst.append(vertex.profile.id)
            elif vertex.profile.follow_request.filter(id=request.user.id).exists():
                request_lst.append(vertex.profile.id)
            else:
                result.append(vertex.profile)
            print(vertex.profile.user.username,
                  vertex.parent.profile.user.username, vertex.distance)
    context = {
        't': result,
        'lst': lst,
        'request_lst': request_lst
    }
    for profile in result:
        print(profile.user.username)
    return render(request, 'users/findFriends.html', context)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        following = False
        requested = False
        if profile.following.filter(id=self.request.user.id).exists():
            following = True
        elif profile.follow_request.filter(id=self.request.user.id).exists():
            requested = True
        context["following"] = following
        context['requested'] = requested
        context['posts'] = Post.objects.all()
        return context


def webcam(request):
    return render(request, 'users/headshot.html')


def postHeadShot(request):
    if request.method == 'POST':
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        import base64
        from django.core.files.base import ContentFile
        format, imgstr = post_data['imageString'].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        file_name = request.user.username+'.'+ext
        request.user.profile.face.save(file_name, data, save=True)
        if fi.faceCapture(request):
            request.user.profile.face.delete(save=True)
            return HttpResponseRedirect(reverse('blog-home'))
        request.user.profile.face.delete(save=True)
        messages.error(
            request, 'Face could not be encoded! Make sure your face is visible')
    return HttpResponseRedirect(reverse('profile'))
