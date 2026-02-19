from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from movies.models import Movie, Show, Theatre
from bookings.models import Booking, Seat
from payments.models import Payment
from events.models import Event, Venue


def dashboard_home(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    total_movies = Movie.objects.count()
    total_shows = Show.objects.count()
    total_bookings = Booking.objects.count()
    total_events = Event.objects.count()
    total_users = User.objects.count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    recent_bookings = Booking.objects.select_related(
        'user', 'show__movie', 'show__theatre'
    ).order_by('-created_at')[:8]

    revenue = Payment.objects.filter(status='SUCCESS').aggregate(
        total=Sum('booking__show__price')
    )['total'] or 0

    context = {
        'total_movies': total_movies,
        'total_shows': total_shows,
        'total_bookings': total_bookings,
        'total_events': total_events,
        'total_users': total_users,
        'confirmed_bookings': confirmed_bookings,
        'recent_bookings': recent_bookings,
        'revenue': revenue,
        'section': 'home',
    }
    return render(request, 'dashboard/home.html', context)


# ── MOVIES ──────────────────────────────────────────────

@staff_member_required(login_url='login')
def movie_list(request):
    movies = Movie.objects.all().order_by('-id')
    return render(request, 'dashboard/movies/list.html', {
        'movies': movies, 'section': 'movies'
    })


@staff_member_required(login_url='login')
def movie_add(request):
    if request.method == 'POST':
        Movie.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            duration=request.POST['duration'],
            language=request.POST['language'],
            release_date=request.POST['release_date'],
            poster=request.FILES.get('poster'),
            is_active='is_active' in request.POST,
        )
        return redirect('dashboard_movies')
    return render(request, 'dashboard/movies/form.html', {
        'action': 'Add', 'section': 'movies'
    })


@staff_member_required(login_url='login')
def movie_edit(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.title = request.POST['title']
        movie.description = request.POST['description']
        movie.duration = request.POST['duration']
        movie.language = request.POST['language']
        movie.release_date = request.POST['release_date']
        movie.is_active = 'is_active' in request.POST
        if request.FILES.get('poster'):
            movie.poster = request.FILES['poster']
        movie.save()
        return redirect('dashboard_movies')
    return render(request, 'dashboard/movies/form.html', {
        'movie': movie, 'action': 'Edit', 'section': 'movies'
    })


@staff_member_required(login_url='login')
def movie_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.delete()
    return redirect('dashboard_movies')


# ── SHOWS ────────────────────────────────────────────────

@staff_member_required(login_url='login')
def show_list(request):
    shows = Show.objects.select_related('movie', 'theatre').order_by('-show_date', '-show_time')
    return render(request, 'dashboard/shows/list.html', {
        'shows': shows, 'section': 'shows'
    })


@staff_member_required(login_url='login')
def show_add(request):
    movies = Movie.objects.filter(is_active=True)
    theatres = Theatre.objects.all()
    if request.method == 'POST':
        show = Show.objects.create(
            movie_id=request.POST['movie'],
            theatre_id=request.POST['theatre'],
            show_date=request.POST['show_date'],
            show_time=request.POST['show_time'],
            price=request.POST['price'],
            total_seats=request.POST['total_seats'],
            available_seats=request.POST['total_seats'],
        )
        # Auto-generate seats
        _generate_seats(show, int(request.POST['total_seats']))
        return redirect('dashboard_shows')
    return render(request, 'dashboard/shows/form.html', {
        'movies': movies, 'theatres': theatres,
        'action': 'Add', 'section': 'shows'
    })


@staff_member_required(login_url='login')
def show_edit(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    movies = Movie.objects.filter(is_active=True)
    theatres = Theatre.objects.all()
    if request.method == 'POST':
        show.movie_id = request.POST['movie']
        show.theatre_id = request.POST['theatre']
        show.show_date = request.POST['show_date']
        show.show_time = request.POST['show_time']
        show.price = request.POST['price']
        show.save()
        return redirect('dashboard_shows')
    return render(request, 'dashboard/shows/form.html', {
        'show': show, 'movies': movies, 'theatres': theatres,
        'action': 'Edit', 'section': 'shows'
    })


@staff_member_required(login_url='login')
def show_delete(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    if request.method == 'POST':
        show.delete()
    return redirect('dashboard_shows')


def _generate_seats(show, total):
    """Auto-generate seats: rows A-Z, up to 10 per row."""
    import string
    rows = string.ascii_uppercase
    per_row = 10
    count = 0
    for row in rows:
        for num in range(1, per_row + 1):
            if count >= total:
                return
            Seat.objects.get_or_create(
                show=show, row=row, seat_number=str(num)
            )
            count += 1


# ── THEATRES ─────────────────────────────────────────────

@staff_member_required(login_url='login')
def theatre_list(request):
    theatres = Theatre.objects.all().order_by('name')
    return render(request, 'dashboard/theatres/list.html', {
        'theatres': theatres, 'section': 'theatres'
    })


@staff_member_required(login_url='login')
def theatre_add(request):
    if request.method == 'POST':
        Theatre.objects.create(
            name=request.POST['name'],
            city=request.POST['city'],
            address=request.POST['address'],
            total_screens=request.POST.get('total_screens', 1),
        )
        return redirect('dashboard_theatres')
    return render(request, 'dashboard/theatres/form.html', {
        'action': 'Add', 'section': 'theatres'
    })


@staff_member_required(login_url='login')
def theatre_edit(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)
    if request.method == 'POST':
        theatre.name = request.POST['name']
        theatre.city = request.POST['city']
        theatre.address = request.POST['address']
        theatre.total_screens = request.POST.get('total_screens', 1)
        theatre.save()
        return redirect('dashboard_theatres')
    return render(request, 'dashboard/theatres/form.html', {
        'theatre': theatre, 'action': 'Edit', 'section': 'theatres'
    })


@staff_member_required(login_url='login')
def theatre_delete(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)
    if request.method == 'POST':
        theatre.delete()
    return redirect('dashboard_theatres')


# ── EVENTS ───────────────────────────────────────────────

@staff_member_required(login_url='login')
def event_list(request):
    events = Event.objects.select_related('venue').order_by('-event_date')
    return render(request, 'dashboard/events/list.html', {
        'events': events, 'section': 'events'
    })


@staff_member_required(login_url='login')
def event_add(request):
    venues = Venue.objects.all()
    from events.models import EVENT_TYPE_CHOICES
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST['title'],
            event_type=request.POST['event_type'],
            description=request.POST.get('description', ''),
            venue_id=request.POST['venue'] if request.POST.get('venue') else None,
            event_date=request.POST['event_date'],
            event_time=request.POST['event_time'],
            price=request.POST['price'],
            total_seats=request.POST['total_seats'],
            available_seats=request.POST['total_seats'],
            language=request.POST.get('language', ''),
            poster=request.FILES.get('poster'),
            is_active='is_active' in request.POST,
        )
        return redirect('dashboard_events')
    return render(request, 'dashboard/events/form.html', {
        'venues': venues, 'event_types': EVENT_TYPE_CHOICES,
        'action': 'Add', 'section': 'events'
    })


@staff_member_required(login_url='login')
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    venues = Venue.objects.all()
    from events.models import EVENT_TYPE_CHOICES
    if request.method == 'POST':
        event.title = request.POST['title']
        event.event_type = request.POST['event_type']
        event.description = request.POST.get('description', '')
        event.venue_id = request.POST['venue'] if request.POST.get('venue') else None
        event.event_date = request.POST['event_date']
        event.event_time = request.POST['event_time']
        event.price = request.POST['price']
        event.total_seats = request.POST['total_seats']
        event.language = request.POST.get('language', '')
        event.is_active = 'is_active' in request.POST
        if request.FILES.get('poster'):
            event.poster = request.FILES['poster']
        event.save()
        return redirect('dashboard_events')
    return render(request, 'dashboard/events/form.html', {
        'event': event, 'venues': venues, 'event_types': EVENT_TYPE_CHOICES,
        'action': 'Edit', 'section': 'events'
    })


@staff_member_required(login_url='login')
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
    return redirect('dashboard_events')


# ── VENUES ───────────────────────────────────────────────

@staff_member_required(login_url='login')
def venue_list(request):
    venues = Venue.objects.all().order_by('name')
    return render(request, 'dashboard/venues/list.html', {
        'venues': venues, 'section': 'venues'
    })


@staff_member_required(login_url='login')
def venue_add(request):
    if request.method == 'POST':
        Venue.objects.create(
            name=request.POST['name'],
            city=request.POST['city'],
            address=request.POST['address'],
            capacity=request.POST.get('capacity', 0),
        )
        return redirect('dashboard_venues')
    return render(request, 'dashboard/venues/form.html', {
        'action': 'Add', 'section': 'venues'
    })


@staff_member_required(login_url='login')
def venue_edit(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == 'POST':
        venue.name = request.POST['name']
        venue.city = request.POST['city']
        venue.address = request.POST['address']
        venue.capacity = request.POST.get('capacity', 0)
        venue.save()
        return redirect('dashboard_venues')
    return render(request, 'dashboard/venues/form.html', {
        'venue': venue, 'action': 'Edit', 'section': 'venues'
    })


@staff_member_required(login_url='login')
def venue_delete(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == 'POST':
        venue.delete()
    return redirect('dashboard_venues')


# ── BOOKINGS ─────────────────────────────────────────────

@staff_member_required(login_url='login')
def booking_list(request):
    bookings = Booking.objects.select_related(
        'user', 'show__movie', 'show__theatre'
    ).prefetch_related('seats').order_by('-created_at')
    return render(request, 'dashboard/bookings/list.html', {
        'bookings': bookings, 'section': 'bookings'
    })


# ── USERS ────────────────────────────────────────────────

@staff_member_required(login_url='login')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users/list.html', {
        'users': users, 'section': 'users'
    })