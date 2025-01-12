from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Concert(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(upload_to='concert_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=20.00)

    def delete(self, *args, **kwargs):
        # Удаление всех связанных бронирований (если это нужно)
        Booking.objects.filter(seat__concert=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

class Seat(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('concert', 'row', 'seat_number')

    def __str__(self):
        return f"Row {self.row} Seat {self.seat_number}"


# Сигнал для автоматического создания схемы зала
@receiver(post_save, sender=Concert)
def create_seating_chart(sender, instance, created, **kwargs):
    if created:
        for row in range(1, 11): 
            for seat in range(1, 13):  
                Seat.objects.create(concert=instance, row=row, seat_number=seat)

class Booking(models.Model):
    seat = models.OneToOneField(Seat, related_name='booking', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.seat} for {self.seat.concert.title}"
