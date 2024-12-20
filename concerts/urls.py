from django.urls import path
from . import views

urlpatterns = [
    path('', views.concert_list, name='concert_list'),
    path('<int:id>/', views.concert_detail, name='concert_detail'),
    path('book/<int:seat_id>/', views.book_seat, name='book_seat'),
]