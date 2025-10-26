from django.db import models
from accounts.models import Wanderer, Walker

class Request(models.Model):
    wanderer = models.ForeignKey(Wanderer, on_delete=models.CASCADE, related_name="requests_sent")
    walker = models.ForeignKey(Walker, on_delete=models.CASCADE, related_name="requests_received")
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.CharField(max_length=20)
    loc_lat = models.FloatField()
    loc_long = models.FloatField()
    fees_paid = models.BooleanField(default=False)
    payment_id = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location_name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"Request from {self.wanderer} to {self.walker}"
