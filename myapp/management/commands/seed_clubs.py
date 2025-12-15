from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Club
import random

class Command(BaseCommand):
    help = "Seed clubs with emojis and mock members"

    def handle(self, *args, **kwargs):
        # Define some sample clubs
        clubs_data = [
            {"name": "Chess Club", "description": "Play and learn chess!", "emoji": "♟️"},
            {"name": "Book Club", "description": "Discuss your favorite books.", "emoji": "📚"},
            {"name": "Music Club", "description": "Jam sessions and music events.", "emoji": "🎵"},
            {"name": "Coding Club", "description": "Learn to code together.", "emoji": "💻"},
            {"name": "Art Club", "description": "Express your creativity.", "emoji": "🎨"},
        ]

        # Clear existing clubs (optional)
        Club.objects.all().delete()

        # Create clubs and assign random members
        users = list(User.objects.all())
        for c in clubs_data:
            club, created = Club.objects.get_or_create(
                name=c["name"],
                defaults={
                    "description": c["description"],
                    "emoji": c["emoji"],
                }
            )

            # Randomly add 0-3 members
            if users:
                members_sample = random.sample(users, k=min(len(users), random.randint(0, 3)))
                club.members.set(members_sample)

            club.save()
            self.stdout.write(self.style.SUCCESS(f"Created club: {club.name} with {club.members.count()} members"))
