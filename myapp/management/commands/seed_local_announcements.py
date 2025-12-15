from django.core.management.base import BaseCommand
from myapp.models import Announcement

class Command(BaseCommand):
    help = 'Seed local announcements for testing'

    def handle(self, *args, **kwargs):
        announcements = [
            "Welcome to our local server!",
            "Don't forget to check out the latest updates.",
            "New features are coming soon!",
        ]

        for text in announcements:
            announcement, created = Announcement.objects.get_or_create(
                body=body
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created announcement: {body}"))
            else:
                self.stdout.write(self.style.WARNING(f"Announcement already exists: {body}"))

        self.stdout.write(self.style.SUCCESS("Finished seeding announcements!"))
