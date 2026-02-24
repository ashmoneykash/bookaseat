from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

from .models import Event, EVENT_TYPE_CHOICES
from bookings.models import EventBooking


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


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity < 1:
            messages.error(request, 'Please select at least 1 ticket.')
            return render(request, 'events/book_event.html', {'event': event})

        if quantity > 10:
            messages.error(request, 'You can book a maximum of 10 tickets at once.')
            return render(request, 'events/book_event.html', {'event': event})

        if quantity > event.available_seats:
            messages.error(request, f'Only {event.available_seats} seat(s) available.')
            return render(request, 'events/book_event.html', {'event': event})

        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=event_id)

            if quantity > event.available_seats:
                messages.error(request, 'Sorry, seats were just taken. Please try again.')
                return render(request, 'events/book_event.html', {'event': event})

            total = event.price * quantity

            booking = EventBooking.objects.create(
                user=request.user,
                event=event,
                quantity=quantity,
                total_price=total,
                status='CONFIRMED',
            )

            event.available_seats -= quantity
            event.save()

        # ================= SEND EVENT TICKET EMAIL =================
        if request.user.email:
            send_mail(
                subject="🎟️ Your Event Ticket - BookASeat",
                message=(
                    f"Hi {request.user.username},\n\n"
                    f"Your event booking is CONFIRMED!\n\n"
                    f"🎤 Event: {event.title}\n"
                    f"📍 Venue: {event.venue.name}\n"
                    f"🎫 Tickets: {booking.quantity}\n"
                    f"📅 Date: {event.event_date}\n"
                    f"⏰ Time: {event.event_time}\n\n"
                    f"Enjoy the event!\n\n"
                    f"— Team BookASeat"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
        # ===========================================================

        return redirect('event_booking_success', booking_id=booking.id)

    return render(request, 'events/book_event.html', {'event': event})


@login_required
def event_booking_success(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id, user=request.user)
    return render(request, 'events/booking_success.html', {'booking': booking})