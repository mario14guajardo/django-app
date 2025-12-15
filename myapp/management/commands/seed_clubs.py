from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Club
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed clubs with emojis and mock members (auto-create users if needed)"

    def handle(self, *args, **kwargs):
        # Sample clubs
        clubs_data = [
            {"name": "Chess Club", "description": "Play and learn chess!", "emoji": "♟️"},
            {"name": "Book Club", "description": "Discuss your favorite books.", "emoji": "📚"},
            {"name": "Music Club", "description": "Jam sessions and music events.", "emoji": "🎵"},
            {"name": "Coding Club", "description": "Learn to code together.", "emoji": "💻"},
            {"name": "Art Club", "description": "Express your creativity.", "emoji": "🎨"},
        ]

        # Clear existing clubs (optional)
        Club.objects.all().delete()

        # Ensure at least 10 users exist for member assignment
        existing_users = list(User.objects.all())
        required_users = 10
        if len(existing_users) < required_users:
            for _ in range(required_users - len(existing_users)):
                username = fake.user_name()
                email = fake.email()
                user = User.objects.create_user(username=username, email=email, password="password123")
                existing_users.append(user)
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

        # Create clubs and assign random members
        for c in clubs_data:
            club, created = Club.objects.get_or_create(
                name=c["name"],
                defaults={
                    "description": c["description"],
                    "emoji": c["emoji"],
                }
            )

            # Randomly assign 3–7 members
            members_sample = random.sample(existing_users, k=random.randint(3, min(7, len(existing_users))))
            club.members.set(members_sample)
            club.save()

            self.stdout.write(self.style.SUCCESS(
                f"Created club: {club.name} with {club.members.count()} members"
            ))

        self.stdout.write(self.style.SUCCESS("✅ Club seeding completed successfully!"))
