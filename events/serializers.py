from rest_framework import serializers
from .models import Event, Attendee
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'start_time', 'end_time', 'max_capacity']
    
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        if data['start_time'] < timezone.now():
            raise serializers.ValidationError("Start time must be in the future")
        return data
    
    def validate_max_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1")
        return value

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email', 'registered_at']
    
    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Invalid email address")
        return value.lower()

class RegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    
    def validate_email(self, value):
        return AttendeeSerializer().validate_email(value)