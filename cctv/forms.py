from django import forms
from .models import Branch, Camera


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = [
            'branch',
            'name',
            'rtsp_url',
            'active'
        ]