from myapp.models import Club
from django.contrib.auth.models import User

def seed_clubs():
    user = User.objects.first()  # Assign first user as creator

    clubs = [
        {"name": "Photography Club", "description": "Capture the world through your lens.", "emoji": "📸"},
        {"name": "Chess Club", "description": "Challenge your mind and play chess with others.", "emoji": "♟️"},
        {"name": "Book Club", "description": "Discuss your favorite books and authors.", "emoji": "📚"},
        {"name": "Coding Club", "description": "Collaborate on projects and learn new skills.", "emoji": "💻"},
        {"name": "Fitness Club", "description": "Stay healthy and motivated together.", "emoji": "🏋️‍♂️"},
    ]

    for c in clubs:
        club, created = Club.objects.get_or_create(
            name=c["name"],
            defaults={
                "description": c["description"],
                "emoji": c["emoji"],
                "created_by": user,
            }
        )
        print(f"{'Created' if created else 'Exists'} club: {c['name']}")

    print("✅ Finished seeding clubs.")
