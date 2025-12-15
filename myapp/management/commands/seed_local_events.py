from django.core.management.base import BaseCommand
from myapp.models import Event
from datetime import datetime

class Command(BaseCommand):
    help = "Seed the database with local events"

    def handle(self, *args, **kwargs):
        local_events = [
            {
                "title": "Local Meetup",
                "description": "A fun meetup for local community members.",
                "date": datetime(2025, 12, 20),  # no time field
            },
            {
                "title": "Tech Workshop",
                "description": "Learn about Django and Python.",
                "date": datetime(2025, 12, 22),
            },
        ]

        for ev in local_events:
            event, created = Event.objects.get_or_create(
                title=ev["title"],
                date=ev["date"],  # only title & date now
                defaults={
                    "description": ev.get("description", ""),
                    "created_by": None,  # or assign a user if needed
                    "image": "",  # optional placeholder
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created event: {ev['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Event already exists: {ev['title']}"))
