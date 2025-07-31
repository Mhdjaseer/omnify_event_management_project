from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import pytz

class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_time']
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F('end_time')),
                name="event_start_before_end"
            ),
            models.UniqueConstraint(
                fields=['name', 'location', 'start_time'],
                name='unique_event_schedule'
            )
        ]
    def __str__(self):
        return f"{self.name} at {self.location}"
    
    @property
    def current_attendee_count(self):
        return self.attendees.count()
    
    def is_full(self):
        return self.current_attendee_count >= self.max_capacity
    
    def convert_timezone(self, timezone_str):
        """More robust timezone conversion"""
        try:
            tz = pytz.timezone(timezone_str)
            return {
                'start_time': self.start_time.astimezone(tz).isoformat(),
                'end_time': self.end_time.astimezone(tz).isoformat()
            }
        except pytz.UnknownTimeZoneError:
            return {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat()
            }

class Attendee(models.Model):
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'email']
        ordering = ['registered_at']
        indexes = [
            models.Index(fields=['event', 'email']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"