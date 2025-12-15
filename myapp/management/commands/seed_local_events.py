from django.core.management.base import BaseCommand
from myapp.models import Event
from datetime import date

class Command(BaseCommand):
    help = 'Seed local events for testing'

    def handle(self, *args, **kwargs):
        events = [
            {
                "title": "Local Meetup",
                "description": "Community meetup event",
                "date": date(2025, 12, 20),
            },
            {
                "title": "Workshop",
                "description": "Hands-on workshop",
                "date": date(2025, 12, 25),
            },
        ]

        for ev in events:
            obj, created = Event.objects.get_or_create(
                title=ev["title"],
                date=ev["date"],
                defaults={
                    "description": ev["description"],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created event: {ev['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Event exists: {ev['title']}"))
