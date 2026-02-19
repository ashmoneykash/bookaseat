from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),

    # Movies
    path('movies/', views.movie_list, name='dashboard_movies'),
    path('movies/add/', views.movie_add, name='dashboard_movie_add'),
    path('movies/<int:movie_id>/edit/', views.movie_edit, name='dashboard_movie_edit'),
    path('movies/<int:movie_id>/delete/', views.movie_delete, name='dashboard_movie_delete'),

    # Shows
    path('shows/', views.show_list, name='dashboard_shows'),
    path('shows/add/', views.show_add, name='dashboard_show_add'),
    path('shows/<int:show_id>/edit/', views.show_edit, name='dashboard_show_edit'),
    path('shows/<int:show_id>/delete/', views.show_delete, name='dashboard_show_delete'),

    # Theatres
    path('theatres/', views.theatre_list, name='dashboard_theatres'),
    path('theatres/add/', views.theatre_add, name='dashboard_theatre_add'),
    path('theatres/<int:theatre_id>/edit/', views.theatre_edit, name='dashboard_theatre_edit'),
    path('theatres/<int:theatre_id>/delete/', views.theatre_delete, name='dashboard_theatre_delete'),

    # Events
    path('events/', views.event_list, name='dashboard_events'),
    path('events/add/', views.event_add, name='dashboard_event_add'),
    path('events/<int:event_id>/edit/', views.event_edit, name='dashboard_event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete, name='dashboard_event_delete'),

    # Venues
    path('venues/', views.venue_list, name='dashboard_venues'),
    path('venues/add/', views.venue_add, name='dashboard_venue_add'),
    path('venues/<int:venue_id>/edit/', views.venue_edit, name='dashboard_venue_edit'),
    path('venues/<int:venue_id>/delete/', views.venue_delete, name='dashboard_venue_delete'),

    # Bookings & Users (read-only)
    path('bookings/', views.booking_list, name='dashboard_bookings'),
    path('users/', views.user_list, name='dashboard_users'),
]