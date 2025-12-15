# myapp/seeds/seed_badges.py

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
        {
            "name": "Early Bird",
            "description": "Login before 9 AM.",
            "image_url": "https://via.placeholder.com/150?text=Early+Bird",
            "unlocked": False,
        },
        {
            "name": "Night Owl",
            "description": "Login after 10 PM.",
            "image_url": "https://via.placeholder.com/150?text=Night+Owl",
            "unlocked": False,
        },
        {
            "name": "Trailblazer",
            "description": "Complete your first challenge.",
            "image_url": "https://via.placeholder.com/150?text=Trailblazer",
            "unlocked": False,
        },
    ]

    for b in badges:
        badge, created = Badge.objects.get_or_create(
            name=b["name"],
            defaults={
                "description": b["description"],
                "unlocked": b["unlocked"],
            },
        )
        # Set or update image
        badge.image = b["image_url"]
        badge.save()
        if created:
            print(f"Created badge: {b['name']}")
        else:
            print(f"Badge already exists: {b['name']}")

    print("✅ Finished seeding badges.")
