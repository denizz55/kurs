from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import logout_view
from .views import profile_view, cancel_booking

urlpatterns = [
    path('', views.concert_list, name='concert_list'),
    path('<int:id>/', views.concert_detail, name='concert_detail'),
    path('book/<int:seat_id>/', views.book_seat, name='book_seat'),  # Этот маршрут для бронирования
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('login/', auth_views.LoginView.as_view(template_name='concerts/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]
