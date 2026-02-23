from django.shortcuts import render, get_object_or_404
from bookings.models import Booking
from .models import Payment


def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    total = booking.seats.count() * booking.show.price

    payment, _ = Payment.objects.get_or_create(
    booking=booking,
    defaults={
        'status': 'SUCCESS',
        'amount': total,
    }
)

    return render(request, 'payments/success.html', {
        'payment': payment,
        'booking': booking,
    })