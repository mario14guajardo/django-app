from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from myapp.models import Post

class Command(BaseCommand):
    help = "Create example posts for LOCAL development only"

    def handle(self, *args, **kwargs):
        # Only run in DEBUG mode
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR("DEBUG=False. Refusing to seed data."))
            return

        # Skip if posts already exist
        if Post.objects.exists():
            self.stdout.write(self.style.WARNING("Posts already exist. Skipping."))
            return

        # Create or get demo user
        user, _ = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com"}
        )

        # ✅ All post creation must be here, inside handle()
        Post.objects.create(
            author=user,
            title="Welcome to the App 👋",
            content="This example post only exists on the local server."
        )

        Post.objects.create(
            author=user,
            title="Local Development Post",
            content="These posts will never appear on Railway."
        )

        self.stdout.write(self.style.SUCCESS("✅ Local example posts created."))
