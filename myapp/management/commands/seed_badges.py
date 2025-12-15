# myapp/management/commands/seed_badges.py
from myapp.models import Badge

def seed_badges():
    badges = [
        {"name": "First Post", "description": "Create your first post!", "emoji": "📝", "unlocked": True},
        {"name": "Contributor", "description": "Create 10 posts.", "emoji": "✍️", "unlocked": False},
        {"name": "Event Attendee", "description": "Participate in your first event.", "emoji": "🎉", "unlocked": False},
        {"name": "Popular Post", "description": "Receive 10 likes on a post.", "emoji": "👍", "unlocked": False},
        {"name": "Community Helper", "description": "Comment on 5 posts.", "emoji": "🤝", "unlocked": False},
    ]

    for b in badges:
        badge, created = Badge.objects.get_or_create(
            name=b["name"],
            defaults={
                "description": b["description"],
                "emoji": b["emoji"],
                "unlocked": b["unlocked"],
            }
        )
        if not created:
            badge.description = b["description"]
            badge.emoji = b["emoji"]
            badge.unlocked = b["unlocked"]
            badge.save()

        print(f"{'Created' if created else 'Updated'} badge: {b['name']}")

    print("✅ Finished seeding badges.")
