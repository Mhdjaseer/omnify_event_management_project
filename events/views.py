from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer, RegistrationSerializer
from .services import EventService, RegistrationService
from django.utils import timezone
import pytz
import logging

logger = logging.getLogger(__name__)

class EventPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = 'start_time'

class ErrorResponse(Response):
    def __init__(self, message, status=status.HTTP_400_BAD_REQUEST):
        logger.error(f"ErrorResponse: {message}")
        super().__init__({"error": message}, status=status)

class EventListCreate(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    pagination_class = EventPagination

    def get_queryset(self):
        logger.info("Fetching upcoming events")
        return EventService.get_upcoming_events()

    def create(self, request, *args, **kwargs):
        logger.info("Creating a new event")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            event = EventService.create_event(serializer.validated_data)
            headers = self.get_success_headers(serializer.data)
            logger.info(f"Event created successfully: {event}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.exception("Failed to create event")
            return ErrorResponse(str(e))

    def list(self, request, *args, **kwargs):
        timezone_str = request.query_params.get('timezone', 'Asia/Kolkata')
        logger.info(f"Listing events with timezone: {timezone_str}")
        
        try:
            tz = pytz.timezone(timezone_str)
            queryset = self.filter_queryset(self.get_queryset())
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                response_data = {
                    'current_time': timezone.now().astimezone(tz).isoformat(),
                    'timezone': timezone_str,
                    'events': serializer.data
                }
                logger.info("Paginated event list returned")
                return self.get_paginated_response(response_data)
            
            serializer = self.get_serializer(queryset, many=True)
            logger.info("Full event list returned")
            return Response({
                'current_time': timezone.now().astimezone(tz).isoformat(),
                'timezone': timezone_str,
                'events': serializer.data
            })
            
        except pytz.UnknownTimeZoneError:
            logger.warning("Invalid timezone provided")
            return ErrorResponse('Invalid timezone provided')

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_url_kwarg = 'pk'

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving event with ID: {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating event with ID: {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting event with ID: {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)

@api_view(['POST'])
def register_attendee(request, pk):
    logger.info(f"Registering attendee for event ID: {pk}")
    event = get_object_or_404(Event, pk=pk)
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        attendee = RegistrationService.register_attendee(
            event.id, 
            serializer.validated_data
        )
        logger.info(f"Attendee registered: {attendee}")
        return Response(
            AttendeeSerializer(attendee).data,
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        logger.exception("Attendee registration failed")
        return ErrorResponse(str(e))

class AttendeeList(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    pagination_class = EventPagination

    def get_queryset(self):
        event_id = self.kwargs['pk']
        logger.info(f"Fetching attendees for event ID: {event_id}")
        event = get_object_or_404(Event, pk=event_id)
        return RegistrationService.get_attendees_for_event(event.id)
