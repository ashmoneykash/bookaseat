from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    language = models.CharField(max_length=50)
    release_date = models.DateField()
    poster = models.ImageField(upload_to='movies/posters/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Theatre(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    total_screens = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} - {self.city}"
    

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='shows')

    show_date = models.DateField()
    show_time = models.TimeField()

    price = models.DecimalField(max_digits=8,decimal_places=2)

    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.theatre.name} - {self.show_date} {self.show_time}"