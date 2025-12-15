from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Profile, Event

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'community']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        labels = {
            'avatar_url': 'Profile Picture URL',
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
