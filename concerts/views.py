from django.shortcuts import render, get_object_or_404
from .models import Concert, Seat
from django.http import HttpResponseRedirect
from django.urls import reverse

def concert_list(request):
    concerts = Concert.objects.order_by('date')
    return render(request, 'concerts/concert_list.html', {'concerts': concerts})

def concert_detail(request, id):
    concert = get_object_or_404(Concert, id=id)
    seats = concert.seats.order_by('row', 'seat_number')
    return render(request, 'concerts/concert_detail.html', {'concert': concert, 'seats': seats})

def book_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if not seat.is_booked:
        seat.is_booked = True
        seat.save()
    return HttpResponseRedirect(reverse('concert_detail', args=[seat.concert.id]))