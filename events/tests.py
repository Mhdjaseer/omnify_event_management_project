from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import json
from .models import Event, Attendee


class EventAPITestCase(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            location="Test Location",
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            max_capacity=2,
        )

        # Default attendee data for POST requests
        self.attendee_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }

        # Optional: Create 2 attendees for list test
        # Attendee.objects.create(name="Alice", email="alice@example.com", event=self.event)
        # Attendee.objects.create(name="Bob", email="bob@example.com", event=self.event)

    def test_create_event(self):
        url = reverse("events:event-list")
        data = {
            "name": "New Event",
            "location": "Online",
            "start_time": timezone.now() + timedelta(days=3),
            "end_time": timezone.now() + timedelta(days=4),
            "max_capacity": 10
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_get_event_list(self):
        url = reverse("events:event-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_get_event_detail(self):
        url = reverse("events:event-detail", args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.event.name)

    def test_update_event(self):
        url = reverse("events:event-detail", args=[self.event.id])
        updated_data = {
            "name": "Updated Event",
            "location": self.event.location,
            "start_time": self.event.start_time.isoformat(),
            "end_time": self.event.end_time.isoformat(),
            "max_capacity": self.event.max_capacity
        }
        response = self.client.put(url, data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Updated Event")

    def test_delete_event(self):
        url = reverse("events:event-detail", args=[self.event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_register_attendee(self):
        # Make a fresh event with no attendees
        event = Event.objects.create(
            name="Open Slot Event",
            location="Somewhere",
            start_time=timezone.now() + timezone.timedelta(hours=3),
            end_time=timezone.now() + timezone.timedelta(hours=4),
            max_capacity=5,
        )
        self.assertEqual(event.attendees.count(), 0)
        self.assertEqual(event.max_capacity, 5)
        url = reverse("events:event-register", args=[event.id])
        response = self.client.post(
            url,
            data=json.dumps(self.attendee_data),
            content_type='application/json'
        )
        # print("Response status:", response.status_code)
        # print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event.refresh_from_db()
        self.assertEqual(event.attendees.count(), 1)



    def test_register_attendee_event_full(self):
        # Fill the event
        Attendee.objects.create(event=self.event, name="A", email="a@example.com")
        Attendee.objects.create(event=self.event, name="B", email="b@example.com")

        url = reverse("events:event-register", args=[self.event.id])
        response = self.client.post(url, self.attendee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Event is full", response.data['error'])

    def test_get_attendee_list(self):
        Attendee.objects.all().delete()  # 🔑 clear existing data

        Attendee.objects.create(event=self.event, name="John", email="john@example.com")
        Attendee.objects.create(event=self.event, name="Jane", email="jane@example.com")

        url = reverse("events:event-attendees", args=[self.event.id])
        response = self.client.get(url)
        print(response,"this is the response !!")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
