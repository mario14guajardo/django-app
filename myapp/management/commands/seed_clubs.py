from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Club, Post


class Command(BaseCommand):
    help = "Seed posts for clubs"

    def handle(self, *args, **kwargs):
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("No users exist"))
            return

        chess = Club.objects.get(name="Chess Club")
        art = Club.objects.get(name="Art Club")

        Post.objects.create(
            title="Welcome to Chess Club",
            body="Talk strategy, openings, and tournaments here ♟️",
            author=user,
            club=chess
        )

        Post.objects.create(
            title="Chess Puzzle of the Week",
            body="White to move and mate in 2.",
            author=user,
            club=chess
        )

        Post.objects.create(
            title="Art Club Kickoff",
            body="Post your drawings, paintings, and digital art 🎨",
            author=user,
            club=art
        )

        self.stdout.write(self.style.SUCCESS("✅ Club posts seeded"))
