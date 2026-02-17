from django.urls import path
from . import views

urlpatterns = [
    path('<int:show_id>/', views.book_show, name='book_show'),
]
