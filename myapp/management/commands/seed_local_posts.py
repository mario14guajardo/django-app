from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from myapp.models import Post
from faker import Faker

class Command(BaseCommand):
    help = "Create example posts for LOCAL development only"

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing posts before creating new ones',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of example posts to create (default 10)',
        )

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR("DEBUG=False. Refusing to seed data."))
            return

        reset = kwargs['reset']
        count = kwargs['count']

        if reset:
            Post.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing posts deleted."))

        elif Post.objects.exists():
            self.stdout.write(self.style.WARNING("Posts already exist. Skipping."))
            return

        fake = Faker()

        # Create a demo user
        user, _ = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com"}
        )

        # Generate fake posts
        for _ in range(count):
            Post.objects.create(
                author=user,
                title=fake.sentence(nb_words=6),
                body=fake.paragraph(nb_sentences=5)
            )

        self.stdout.write(self.style.SUCCESS(f"✅ {count} local example posts created."))
