from .models import Event, Attendee
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import IntegrityError

class EventService:
    @staticmethod
    def create_event(event_data):
        event = Event(**event_data)
        try:
            event.full_clean()
            event.save()
            return event
        except IntegrityError:
            raise ValidationError("An event with the same name, location, and start time already exists.")
    
    @staticmethod
    def get_upcoming_events():
        return Event.objects.filter(start_time__gt=timezone.now()).order_by('start_time')

class RegistrationService:
    @staticmethod
    def register_attendee(event_id, attendee_data):
        event = Event.objects.get(pk=event_id)
        
        if event.is_full():
            raise ValidationError("This event has reached maximum capacity")
        
        if Attendee.objects.filter(event=event, email=attendee_data['email']).exists():
            raise ValidationError("This email is already registered for the event")
        
        attendee = Attendee(event=event, **attendee_data)
        attendee.full_clean()
        attendee.save()
        return attendee
    
    @staticmethod
    def get_attendees_for_event(event_id):
        return Attendee.objects.filter(event_id=event_id).select_related('event').order_by('registered_at')