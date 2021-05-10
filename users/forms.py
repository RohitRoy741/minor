from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


BLOCK_CHOICES = [('G1', 'G1'), ('G2', 'G2'), ('G3', 'G3'), ('B1', 'B1'),
                 ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'), ('B6', 'B6'), ('B7', 'B7')]

PROGRAMME_CHOICES = [('B.Tech', 'B.tech'), ('M.Tech', 'M.tech'),
                     ('BJMC', 'BJMC'), ('BA', 'BA'), ('BSc', 'Bsc')]

BRANCH_CHOICES = [('CSE', 'CSE'), ('IT', 'IT'), ('CCE', 'CCE'), ('ECE', 'ECE'), ('EE', 'EE'), ('Mech', 'Mech'), ('Civil',
                                                                                                                 'Civil'), ('Chemical', 'Chemical'), ('Economics', 'Economics'), ('English', 'English'), ('Psychology', 'Psycology')]


class ProfileUpdateForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}))
    block = forms.CharField(widget=forms.Select(choices=BLOCK_CHOICES))
    programme = forms.CharField(widget=forms.Select(choices=PROGRAMME_CHOICES))
    branch = forms.CharField(widget=forms.Select(choices=BRANCH_CHOICES))

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'two_factor', 'block',
                  'room', 'programme', 'branch', 'dob']
