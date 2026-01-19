from django.db import models
from django.core.exceptions import ValidationError

class Organization(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self): return f"{self.name} ({self.address})" if self.address else self.name

class EventType(models.Model):
    type_name = models.CharField(max_length=50)
    def __str__(self): return self.type_name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    def __str__(self): return self.title

class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")


        if hasattr(self, 'event') and self.event:
            conflicts = Schedule.objects.filter(
                event__date=self.event.date,
                event__location=self.event.location,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)

            if conflicts.exists():
                raise ValidationError("Conflict: This location is already booked for this time!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)