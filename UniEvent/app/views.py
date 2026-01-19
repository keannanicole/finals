from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Event, Schedule
from .form import EventForm, ScheduleForm


def event_dashboard(request):
    events = Event.objects.all().prefetch_related('schedules').order_by('date')
    ScheduleFormSet = inlineformset_factory(Event, Schedule, form=ScheduleForm, extra=1, can_delete=False)

    if request.method == 'POST':
        form = EventForm(request.POST)
        formset = ScheduleFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            event_instance = form.save()
            schedules = formset.save(commit=False)
            for s in schedules:
                s.event = event_instance
                s.save()
            return redirect('event_dashboard')
    else:
        form = EventForm()
        formset = ScheduleFormSet()
    return render(request, 'app/dashboard.html', {'events': events, 'form': form, 'formset': formset})


def add_extra_schedule(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = ScheduleForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_slot = form.save(commit=False)
            new_slot.event = event
            try:
                new_slot.full_clean()
                new_slot.save()
                return redirect('event_dashboard')
            except ValidationError as e:
                form.add_error(None, e)

    return render(request, 'app/add_schedule.html', {'form': form, 'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('event_dashboard')