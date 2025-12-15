from django.core.management.base import BaseCommand
from myapp.models import Event

class Command(BaseCommand):
    help = 'Seed local events for testing'

    def handle(self, *args, **kwargs):
        events = [
            {"title": "Local Meetup", "date": "2025-12-20"},
            {"title": "Workshop on Django", "date": "2025-12-22"},
            {"title": "Community Hackathon", "date": "2025-12-28"},
        ]

        for ev in events:
            event, created = Event.objects.get_or_create(
                title=ev["title"],
                date=ev["date"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created event: {ev['title']} on {ev['date']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Event already exists: {ev['title']}"))

        self.stdout.write(self.style.SUCCESS("Finished seeding events!"))
