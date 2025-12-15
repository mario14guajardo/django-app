from django.db import models
from django.contrib.auth.models import User

# ---------------------- PROFILE ----------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True)
    # Add more fields for UI settings, badges, reputation, etc.

    def __str__(self):
        return self.user.username

# ---------------------- COMMUNITY ----------------------
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# ---------------------- POSTS ----------------------
class Post(models.Model):
    title = models.CharField(max_length=200, default="Untitled")
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name="upvoted_posts", blank=True)

    def __str__(self):
        return self.title

# ---------------------- COMMENTS ----------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"

# ---------------------- EVENTS ----------------------
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
    time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)

    def __str__(self):
        return self.title

# ---------------------- BADGES ----------------------
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="badges/", blank=True, null=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
