from django.db import transaction
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from movies.models import Show
from .models import Seat, Booking, EventBooking

@login_required
def book_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    seats = show.seats.annotate(
            seat_num_int=Cast('seat_number', IntegerField())
        ).order_by('row', 'seat_num_int')

    if request.method == 'POST':
        print(request.POST)

        selected_seat_ids = request.POST.getlist('seats')

        if not selected_seat_ids:
            return render(request, 'bookings/book_show.html', {
                'show': show,
                'seats': seats,
                'error': 'Please select at least one seat.'
            })

        with transaction.atomic():

            # Check if any seat is already booked
            already_booked = Seat.objects.filter(
                id__in=selected_seat_ids,
                seat_bookings__status='CONFIRMED'
            ).exists()

            if already_booked:
                return render(request, 'bookings/book_show.html', {
                    'show': show,
                    'seats': seats,
                    'error': 'One or more selected seats are already booked.'
                })

            booking = Booking.objects.create(
                user=request.user,
                show=show,
                status='PENDING'
            )

            for seat_id in selected_seat_ids:
                seat = Seat.objects.get(id=seat_id)
                booking.seats.add(seat)

            booking.status = 'CONFIRMED'
            booking.save()

            show.available_seats -= len(selected_seat_ids)
            show.save()

        return redirect('payment_success', booking_id=booking.id)

    return render(request, 'bookings/book_show.html', {
        'show': show,
        'seats': seats
    })


@login_required
def my_bookings(request):
    movie_bookings = Booking.objects.filter(user=request.user).select_related(
        'show', 'show__movie', 'show__theatre'
    ).prefetch_related('seats').order_by('-id')

    event_bookings = EventBooking.objects.filter(user=request.user).select_related(
        'event', 'event__venue'
    ).order_by('-id')

    return render(request, 'bookings/my_bookings.html', {
        'movie_bookings': movie_bookings,
        'event_bookings': event_bookings,
    })