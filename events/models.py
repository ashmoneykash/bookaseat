from django.db import models


EVENT_TYPE_CHOICES = [
    ('concert', 'Concert'),
    ('sport', 'Sport'),
    ('comedy', 'Comedy'),
    ('theatre', 'Theatre'),
    ('festival', 'Festival'),
    ('other', 'Other'),
]


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} — {self.city}"


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, related_name='events')
    event_date = models.DateField()
    event_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=100)
    available_seats = models.PositiveIntegerField(default=100)
    poster = models.ImageField(upload_to='events/posters/', blank=True, null=True)
    language = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()}) — {self.event_date}"