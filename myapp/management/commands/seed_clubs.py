from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Club, Post
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed clubs with emojis, random members, and posts."

    def handle(self, *args, **kwargs):
        # ----------------- CLUBS -----------------
        clubs_data = [
            {"name": "Chess Club", "description": "Play and learn chess!", "emoji": "♟️"},
            {"name": "Book Club", "description": "Discuss your favorite books.", "emoji": "📚"},
            {"name": "Music Club", "description": "Jam sessions and music events.", "emoji": "🎵"},
            {"name": "Coding Club", "description": "Learn to code together.", "emoji": "💻"},
            {"name": "Art Club", "description": "Express your creativity.", "emoji": "🎨"},
        ]

        # Optional: Clear existing clubs and posts
        Post.objects.all().delete()
        Club.objects.all().delete()

        # ----------------- USERS -----------------
        existing_users = list(User.objects.all())
        required_users = 10
        if len(existing_users) < required_users:
            for _ in range(required_users - len(existing_users)):
                username = fake.user_name()
                email = fake.email()
                user = User.objects.create_user(username=username, email=email, password="password123")
                existing_users.append(user)
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

        # ----------------- CREATE CLUBS -----------------
        for c in clubs_data:
            club, created = Club.objects.get_or_create(
                name=c["name"],
                defaults={
                    "description": c["description"],
                    "emoji": c["emoji"],
                    "created_by": random.choice(existing_users)
                }
            )

            # Assign random members (3–7)
            members_sample = random.sample(existing_users, k=random.randint(3, min(7, len(existing_users))))
            club.members.set(members_sample)
            club.save()
            self.stdout.write(self.style.SUCCESS(
                f"Created club: {club.name} with {club.members.count()} members"
            ))

            # ----------------- CREATE POSTS -----------------
            for i in range(random.randint(2, 5)):  # 2–5 posts per club
                post = Post.objects.create(
                    title=f"{club.name} Post {i+1}",
                    body=fake.paragraph(nb_sentences=5),  # use `body`, not `content`
                    author=random.choice(members_sample),
                    community=None,  # optional, since these are club posts
                )
                # Optionally, associate posts with the club through ManyToMany if needed
                # For now, just store club reference in the title/body if needed
                self.stdout.write(self.style.SUCCESS(f"Created post: {post.title} for {club.name}"))

        self.stdout.write(self.style.SUCCESS("✅ Clubs, members, and posts seeded successfully!"))
