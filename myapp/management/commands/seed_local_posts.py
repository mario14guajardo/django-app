from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Post
import random

class Command(BaseCommand):
    help = "Seed GLOBAL posts for home/feed"

    def handle(self, *args, **kwargs):
        if Post.objects.filter(club__isnull=True, community__isnull=True).exists():
            self.stdout.write(self.style.WARNING("Global posts already exist. Skipping."))
            return

        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("No users found. Create users first."))
            return

        posts = [
            ("Welcome to the Campus App", "This is a public post visible to everyone."),
            ("Lost & Found", "Found a calculator near the library."),
            ("Best Study Spots?", "Any recommendations for quiet places to study?"),
            ("Finals Week Tips", "Good luck everyone — stay hydrated."),
            ("Parking Issues", "Parking Lot C is full again 😭"),
        ]

        for title, body in posts:
            Post.objects.create(
                title=title,
                body=body,
                author=random.choice(users),
                # ⚠️ DO NOT SET club or community
            )

        self.stdout.write(self.style.SUCCESS("Global posts seeded successfully."))
