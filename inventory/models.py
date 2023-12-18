from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Inventory_item(models.Model):
    # item_no = models.IntegerField()
    description = models.TextField()
    quantity = models.FloatField()
    date = models.DateField(default=now, )
    location = models.CharField(max_length=256)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    
    
    def __str__(self):
        return self.location
    
    class Meta:
        ordering = ['-date']
    
    
class Location(models.Model):
    name = models.CharField(max_length=256)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Locations"