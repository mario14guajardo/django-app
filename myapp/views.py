from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Community, Post, Event, Badge, Profile, Comment, Announcement
from .forms import PostForm, CommentForm, ProfileForm, EventForm, RegisterForm


# ---------------------- BASIC PAGES ----------------------

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'myapp/home.html', {
        'posts': posts,
        'announcements': announcements,
    })


def contact(request):
    return render(request, 'myapp/contact.html')


def school_map(request):
    return render(request, 'myapp/school_map.html')


def badges(request):
    badges = Badge.objects.all()
    return render(request, 'myapp/badges.html', {'badges': badges})


# ---------------------- AUTH ----------------------

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "myapp/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid credentials.")

    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------------- COMMUNITY ----------------------

def community_detail(request, name):
    community = get_object_or_404(Community, name=name)
    posts = Post.objects.filter(community=community).order_by('-created_at')
    return render(request, 'myapp/community_detail.html', {
        'community': community,
        'posts': posts
    })


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'myapp/create_post.html', {'form': form})


def create_post_in_community(request, name):
    community = get_object_or_404(Community, name=name)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            return redirect('community_detail', name=community.name)
    else:
        form = PostForm()

    return render(request, 'myapp/create_post_in_community.html', {
        'form': form,
        'community': community
    })


# ---------------------- POSTS ----------------------

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    comments = post.comments.all().order_by("-created_at")

    return render(request, 'myapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


def toggle_upvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.upvotes.all():
        post.upvotes.remove(user)
    else:
        post.upvotes.add(user)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ---------------------- PROFILE ----------------------

@login_required
def user_profile(request, username=None):
    user_obj = get_object_or_404(User, username=username) if username else request.user
    profile, _ = Profile.objects.get_or_create(user=user_obj)
    posts = Post.objects.filter(author=user_obj).order_by('-created_at')

    return render(request, 'myapp/user_profile.html', {
        'profile': profile,
        'posts': posts,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")

        avatar = request.FILES.get("avatar")
        if avatar:
            profile.avatar = avatar
            profile.save()

        request.user.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")

    return render(request, "myapp/edit_profile.html")


@login_required
def reset_avatar(request):
    profile = request.user.profile
    profile.avatar.delete(save=True)
    messages.success(request, "Profile picture has been reset.")
    return redirect("edit_profile")


# ---------------------- EVENTS ----------------------

def events(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'myapp/events.html', {
        'events': events
    })


def submit_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('submit_event_success')
    else:
        form = EventForm()

    return render(request, 'myapp/submit_event.html', {'form': form})


def submit_event_success(request):
    return render(request, 'myapp/submit_event_success.html')


# ---------------------- SEARCH ----------------------

def search(request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(title__icontains=query) if query else []
    return render(request, 'myapp/search_results.html', {
        'query': query,
        'results': results
    })


def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, "myapp/feed.html", {
        "posts": posts,
        "form": form,
    })
