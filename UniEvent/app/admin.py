from django.contrib import admin
from .models import Organization, Location, EventType, Event, Schedule

admin.site.register(Organization)
admin.site.register(Location)
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Schedule)