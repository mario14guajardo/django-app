# myapp/management/commands/seed_badges.py

from myapp.models import Badge

def seed_badges():
    badges = [
        {
            "name": "First Post",
            "description": "Create your first post!",
            "image_url": "https://via.placeholder.com/150?text=First+Post",
            "unlocked": True,
        },
        {
            "name": "Contributor",
            "description": "Create 10 posts.",
            "image_url": "https://via.placeholder.com/150?text=Contributor",
            "unlocked": False,
        },
        {
            "name": "Event Attendee",
            "description": "Participate in your first event.",
            "image_url": "https://via.placeholder.com/150?text=Event+Attendee",
            "unlocked": False,
        },
        {
            "name": "Popular Post",
            "description": "Receive 10 likes on a post.",
            "image_url": "https://via.placeholder.com/150?text=Popular+Post",
            "unlocked": False,
        },
        {
            "name": "Community Helper",
            "description": "Comment on 5 posts.",
            "image_url": "https://via.placeholder.com/150?text=Helper",
            "unlocked": False,
        },
    ]

    for b in badges:
        badge, created = Badge.objects.get_or_create(
            name=b["name"],
            defaults={
                "description": b["description"],
                "image_url": b["image_url"],
                "unlocked": b["unlocked"],
            },
        )
        if not created:
            # Update existing badge in case fields changed
            badge.description = b["description"]
            badge.image_url = b["image_url"]
            badge.unlocked = b["unlocked"]
            badge.save()

        print(f"{'Created' if created else 'Updated'} badge: {b['name']}")

    print("✅ Finished seeding badges.")
