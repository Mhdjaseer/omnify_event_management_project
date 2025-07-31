from django.contrib import admin
from .models import Event, Attendee

class AttendeeInline(admin.TabularInline):
    model = Attendee
    extra = 0
    readonly_fields = ['name', 'email', 'registered_at']
    can_delete = False
    show_change_link = False

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_time', 'end_time', 'max_capacity', 'current_attendee_count')
    list_filter = ('location', 'start_time')
    search_fields = ('name', 'location')
    inlines = [AttendeeInline]
    readonly_fields = ('created_at',)

    def current_attendee_count(self, obj):
        return obj.attendees.count()
    current_attendee_count.short_description = 'Attendees'

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'registered_at')
    list_filter = ('event', 'registered_at')
    search_fields = ('name', 'email', 'event__name')
    readonly_fields = ('registered_at',)
