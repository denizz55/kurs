from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(upload_to='concert_images/')
    hall_map = models.ImageField(upload_to='hall_maps/')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=20.00)


    def __str__(self):
        return self.name

class Seat(models.Model):
    concert = models.ForeignKey(Concert, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=5)  # Row name, e.g., 'A', 'B'
    seat_number = models.IntegerField()  # Seat number
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.row}-{self.seat_number} ({'Booked' if self.is_booked else 'Available'})"

class Booking(models.Model):
    seat = models.OneToOneField(Seat, related_name='booking', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.seat} by {self.user.username}"
