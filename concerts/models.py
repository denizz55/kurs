from django.db import models

class Concert(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(upload_to='concert_images/')
    hall_map = models.ImageField(upload_to='hall_maps/')

    def __str__(self):
        return self.name

class Seat(models.Model):
    concert = models.ForeignKey(Concert, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=5) 
    seat_number = models.IntegerField()  
    is_booked = models.BooleanField(default=False)
