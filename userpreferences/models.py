from django.db import models
from django.contrib.auth.models import User



class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=225, blank=True, null=True, default="USD - United States Dollar")
    
    
    def __str__(self):
        return str(User)+ 's' + 'preferences'