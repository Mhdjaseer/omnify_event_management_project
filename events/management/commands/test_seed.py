from django.core.management.base import BaseCommand
from events.models import Event, Attendee
from faker import Faker
from django.utils import timezone
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Add extra demo Events and Attendees for testing'

    def handle(self, *args, **options):
        self.stdout.write("Adding demo events and attendees...")

        for _ in range(5):  # Add 5 demo events
            start_time = timezone.now() + timezone.timedelta(days=random.randint(1, 10))
            end_time = start_time + timezone.timedelta(hours=random.randint(1, 3))

            event = Event.objects.create(
                name=f"{fake.catch_phrase()} {random.randint(1000,9999)}",  # add unique suffix
                location=fake.city(),
                start_time=start_time,
                end_time=end_time,
                max_capacity=random.randint(10, 50)
            )

            attendee_count = random.randint(3, min(10, event.max_capacity))

            for _ in range(attendee_count):
                try:
                    Attendee.objects.create(
                        event=event,
                        name=fake.name(),
                        email=fake.unique.email()
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to add attendee: {e}"))

        self.stdout.write(self.style.SUCCESS("Demo events and attendees added successfully."))
