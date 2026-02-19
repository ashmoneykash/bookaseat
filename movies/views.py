from django.shortcuts import render, get_object_or_404
from .models import Movie
from events.models import Event


def movie_list(request):
    movies = Movie.objects.filter(is_active=True)
    events = Event.objects.filter(is_active=True).select_related('venue').order_by('event_date')[:8]
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'events': events,
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    shows = movie.shows.all()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'shows': shows,
    })