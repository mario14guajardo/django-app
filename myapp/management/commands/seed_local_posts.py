from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from posts.models import Post

class Command(Base Command):
  help = "Create example posts for LOCAL development only"

  def handle(self, *args, **kwargs):
    if not settings.DEBUG:
      self.stdout.write(self.style.ERROR(
        "DEBUG is False. Refusing to seed data."
      ))
      return
    if Post.objects.exists():
      self.stdout.write(self.style.WARNING(
        "Posts already exist. Skipping seed."
      ))
      return

  user, _ = User.objects.get_or_create(
      username="demo_user",
      defaults={"email": "demo@example.com"}
  )

Post.objects.create(
  author=user,
  title="Welcome to the App 👋",
  content="This is an example post created for local development."
)

Post.objects.create(
  author=user,
  title="Second Example Post",
  content="These posts only exist on the local server."
)

self.stdout.write(self.style.SUCCESS(
  "✅ Local example posts created."
))
