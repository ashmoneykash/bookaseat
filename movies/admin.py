from django.contrib import admin
from .models import Movie, Theatre, Show
# Register your models here.

admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Show)