from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    status = models.CharField(max_length=50, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"
