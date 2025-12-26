from django.db import models
from accounts.models import *

class Room(models.Model):
    walker = models.ForeignKey(Walker,on_delete=models.CASCADE)
    wanderer = models.ForeignKey(Wanderer,on_delete=models.CASCADE)
    start_location_name = models.CharField(max_length=300)
    start_location_latitude = models.FloatField()
    start_location_longitude = models.FloatField()


    def __str__(self):
        return str(self.id)
    
class LiveLocation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null = True,blank = True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'room')


class ScheduledWalks(models.Model):
    walker = models.ForeignKey(Walker,on_delete=models.CASCADE)
    wanderer = models.ForeignKey(Wanderer,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    walk_completed = models.BooleanField(default=False)
    date = models.CharField(max_length=300)
    time = models.CharField(max_length=300)
    start_location_name = models.CharField(max_length=300)
    start_location_latitude = models.FloatField()
    start_location_longitude = models.FloatField()
    payment_id = models.BigIntegerField(blank=True, null=True)




