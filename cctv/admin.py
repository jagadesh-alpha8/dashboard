# cctv/admin.py

from django.contrib import admin
from .models import Branch, Camera

admin.site.register(Branch)
admin.site.register(Camera)