# models.py
from django.db import models
from django.contrib.auth.models import User  # Import the User model

class CapturedPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User
    image = models.ImageField(upload_to='captured_images/')
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description or "Captured Photo"
