from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test demo seeding command'

    def handle(self, *args, **kwargs):
        self.stdout.write("✅ Custom seed_demo command is working")
