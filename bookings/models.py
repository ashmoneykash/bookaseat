from django.db import models
from django.conf import settings


class Seat(models.Model):
    show = models.ForeignKey(
        'movies.Show',
        on_delete=models.CASCADE,
        related_name='seats'
    )
    seat_number = models.CharField(max_length=5)
    row = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.row}{self.seat_number} - {self.show}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    show = models.ForeignKey(
        'movies.Show',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    seats = models.ManyToManyField('Seat', related_name='seat_bookings')
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user}"
