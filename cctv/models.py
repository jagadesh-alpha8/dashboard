# cctv/models.py

from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Camera(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='cameras'
    )

    name = models.CharField(max_length=100)

    rtsp_url = models.TextField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def mediamtx_path(self):
        from django.utils.text import slugify
        return slugify(self.name)