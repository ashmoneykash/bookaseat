from django.db import models

# Create your models here.

class Booking(models.Model):
    movie_name = models.CharField(max_length=100)
    seats = models.IntegerField()
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.movie_name


class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    status = models.CharField(max_length=50, default="created")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.movie_name}"
