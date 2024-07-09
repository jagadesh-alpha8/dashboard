# models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class CapturedPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='captured_images/')
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description or "Captured Photo"

    def delete(self, *args, **kwargs):
        # Delete the image file from the media folder
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(CapturedPhoto, self).delete(*args, **kwargs)
