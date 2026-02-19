from django.shortcuts import render, get_object_or_404
from .models import Event, EVENT_TYPE_CHOICES


def event_list(request):
    event_type = request.GET.get('type', '')
    events = Event.objects.filter(is_active=True)
    if event_type:
        events = events.filter(event_type=event_type)
    return render(request, 'events/event_list.html', {
        'events': events,
        'event_types': EVENT_TYPE_CHOICES,
        'selected_type': event_type,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    return render(request, 'events/event_detail.html', {'event': event})