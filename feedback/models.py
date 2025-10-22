from django.db import models
from accounts.models import Walker, Wanderer  

class WalkerFeedback(models.Model):
    walker = models.ForeignKey(Walker, on_delete=models.CASCADE)
    wanderer = models.ForeignKey(Wanderer, on_delete=models.CASCADE)
    wanderer_name = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback from {self.wanderer_name} to Walker {self.walker.user.email}"


class WandererFeedback(models.Model):
    walker = models.ForeignKey(Walker, on_delete=models.CASCADE)
    wanderer = models.ForeignKey(Wanderer, on_delete=models.CASCADE)
    walker_name = models.TextField(blank=True, null=True)
    rating = models.IntegerField()

    def __str__(self):
        return f"Feedback from Walker {self.walker.user.email} to Wanderer {self.wanderer.user.email}"
