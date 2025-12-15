from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Club, Post
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed clubs with emojis, mock members, and sample posts (auto-create users if needed)"

    def handle(self, *args, **kwargs):
        # Sample clubs
        clubs_data = [
            {"name": "Chess Club", "description": "Play and learn chess!", "emoji": "♟️"},
            {"name": "Book Club", "description": "Discuss your favorite books.", "emoji": "📚"},
            {"name": "Music Club", "description": "Jam sessions and music events.", "emoji": "🎵"},
            {"name": "Coding Club", "description": "Learn to code together.", "emoji": "💻"},
            {"name": "Art Club", "description": "Express your creativity.", "emoji": "🎨"},
        ]

        # Clear existing clubs and posts (optional)
        Post.objects.all().delete()
        Club.objects.all().delete()

        # Ensure at least 10 users exist
        existing_users = list(User.objects.all())
        required_users = 10
        if len(existing_users) < required_users:
            for _ in range(required_users - len(existing_users)):
                username = fake.user_name()
                email = fake.email()
                user = User.objects.create_user(username=username, email=email, password="password123")
                existing_users.append(user)
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

        # Create clubs, assign members, and create posts
        for c in clubs_data:
            club, created = Club.objects.get_or_create(
                name=c["name"],
                defaults={
                    "description": c["description"],
                    "emoji": c["emoji"],
                }
            )

            # Assign 3–7 random members
            members_sample = random.sample(existing_users, k=random.randint(3, min(7, len(existing_users))))
            club.members.set(members_sample)
            club.save()
            self.stdout.write(self.style.SUCCESS(
                f"Created club: {club.name} with {club.members.count()} members"
            ))

            # Create 2–4 posts per club
            for i in range(random.randint(2, 4)):
                author = random.choice(members_sample)
                post = Post.objects.create(
                    title=f"{club.name} Post {i+1}",
                    content=fake.paragraph(nb_sentences=3),
                    author=author,
                    club=club
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Created post: '{post.title}' by {author.username} in {club.name}"
                ))

        self.stdout.write(self.style.SUCCESS("✅ Club seeding with members and posts completed successfully!"))
