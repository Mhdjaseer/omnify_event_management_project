# events/urls.py
from django.urls import path
from .views import (
    EventListCreate,
    EventRetrieveUpdateDestroy,
    register_attendee,
    AttendeeList
)

app_name = 'events' 

urlpatterns = [
    path('api/events/', EventListCreate.as_view(), name='event-list'),
    path('api/events/<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='event-detail'),
    path('api/events/<int:pk>/register/', register_attendee, name='event-register'),
    path('api/events/<int:pk>/attendees/', AttendeeList.as_view(), name='event-attendees'),
]