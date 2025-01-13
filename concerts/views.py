from django.shortcuts import render, get_object_or_404
from .models import Concert, Seat, Booking
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db import IntegrityError
from .forms import ConcertFilterForm

def concert_list(request):
    concerts = Concert.objects.order_by('date')
    form = ConcertFilterForm(request.GET or None)

    if form.is_valid():
        # Фильтрация по дате
        if form.cleaned_data.get('date'):
            concerts = concerts.filter(date__date=form.cleaned_data['date'])
        # Фильтрация по месяцу
        elif form.cleaned_data.get('month'):
            month = form.cleaned_data['month']
            concerts = concerts.filter(
                date__year=month.year,
                date__month=month.month
            )

    return render(request, 'concerts/concert_list.html', {'concerts': concerts, 'form': form})

def concert_detail(request, id):
    concert = get_object_or_404(Concert, id=id)

    # Формирование схемы зала
    rows = Seat.objects.filter(concert=concert).values_list('row', flat=True).distinct()
    seating_chart = {
        row: Seat.objects.filter(concert=concert, row=row).order_by('seat_number')
        for row in rows
    }

    return render(request, 'concerts/concert_detail.html', {
        'concert': concert,
        'seating_chart': seating_chart,
    })

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def book_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    # Проверяем, что место уже забронировано
    if seat.is_booked:
        messages.error(request, 'This seat is already booked.')
        return HttpResponseRedirect(reverse('concert_detail', args=[seat.concert.id]))

    if request.method == 'POST':
        # Проверяем авторизацию пользователя
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to book a seat.')
            return HttpResponseRedirect(reverse('login'))

        # Получаем данные из формы
        try:
            Booking.objects.create(
                seat=seat,
                user=request.user
            )
            seat.is_booked = True
            seat.save()
            messages.success(request, f'Seat {seat.row}-{seat.seat_number} has been successfully booked.')
            return HttpResponseRedirect(reverse('concert_detail', args=[seat.concert.id]))
        except IntegrityError:
            messages.error(request, 'This seat has already been booked by another user.')
            return HttpResponseRedirect(reverse('concert_detail', args=[seat.concert.id]))

    return render(request, 'concerts/book_seat.html', {'seat': seat})
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Проверяем, что пользователь может отменить только свою бронь
    if booking.user != request.user:
        return HttpResponseForbidden('You can only cancel your own bookings.')

    # Отменяем бронь
    seat = booking.seat
    booking.delete()
    seat.is_booked = False
    seat.save()
    messages.success(request, f'Your booking for seat {seat.row}-{seat.seat_number} has been cancelled.')
    return HttpResponseRedirect(reverse('concert_detail', args=[seat.concert.id]))


def cancel_booking(request, booking_id):
    # Получаем бронирование или возвращаем 404
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Освобождаем место
    seat = booking.seat
    seat.is_booked = False
    seat.save()

    # Удаляем бронирование
    booking.delete()

    # Сообщение об успешной отмене бронирования
    messages.success(request, "Бронирование успешно отменено.")
    return redirect('profile')  # Перенаправление в личный кабинет

@login_required
def profile(request):
    # Получаем бронирования текущего пользователя
    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'bookings': bookings,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user) 
            return redirect('concert_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'concerts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('concert_list')  # Перенаправление на главную страницу

def profile_view(request):
    # Получить все бронирования для текущего пользователя
    bookings = Booking.objects.filter(user=request.user).select_related('seat__concert')
    return render(request, 'concerts/profile.html', {'bookings': bookings})