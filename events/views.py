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

class EventPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = 'start_time'

class ErrorResponse(Response):
    def __init__(self, message, status=status.HTTP_400_BAD_REQUEST):
        super().__init__({"error": message}, status=status)

class EventListCreate(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    pagination_class = EventPagination

    def get_queryset(self):
        return EventService.get_upcoming_events()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            event = EventService.create_event(serializer.validated_data)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except ValidationError as e:
            return ErrorResponse(str(e))

    def list(self, request, *args, **kwargs):
        timezone_str = request.query_params.get('timezone', 'Asia/Kolkata')
        
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
                return self.get_paginated_response(response_data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'current_time': timezone.now().astimezone(tz).isoformat(),
                'timezone': timezone_str,
                'events': serializer.data
            })
            
        except pytz.UnknownTimeZoneError:
            return ErrorResponse('Invalid timezone provided')

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_url_kwarg = 'pk'

@api_view(['POST'])
def register_attendee(request, pk):
    event = get_object_or_404(Event, pk=pk)
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        attendee = RegistrationService.register_attendee(
            event.id, 
            serializer.validated_data
        )
        return Response(
            AttendeeSerializer(attendee).data,
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return ErrorResponse(str(e))

class AttendeeList(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    pagination_class = EventPagination

    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return RegistrationService.get_attendees_for_event(event.id)