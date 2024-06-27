from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

import base64
import io
from datetime import datetime
from PIL import Image
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CapturedPhoto
import json


from django.contrib.auth.models import User, Group
from .models import CapturedPhoto
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

from .decorator import group_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .models import CapturedPhoto 

def handler404(request, exception):
    return render(request, 'error.html', status=404)

def user_login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')  
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def contact(request):
    return render(request,'error.html')

@login_required
def home(request):
    if request.method == 'POST':
        selected_option = request.POST.get('bname')  
        if selected_option=='edu1':
            return render(request,'edu1.html')
        elif selected_option=='ingage':
            return render(request,'error.html')
        elif selected_option=='rewin':
            return render(request,'error.html')
    return render(request,'home.html')

@login_required
def edutech(request):
    if request.method == 'POST':
        selected_option = request.POST.get('nm')
        if selected_option == 'NM1':
            src="https://lookerstudio.google.com/embed/reporting/98b3b72e-82d8-400d-bb2e-319fff1f7415/page/FPr1D"
            return render(request, 'nmiframe.html',{'src':src})
        elif selected_option == 'NM2':
            src="https://lookerstudio.google.com/embed/reporting/4f2aea2b-b418-4c22-8488-14d491a3882c/page/gJr1D"
            return render(request, 'nmiframe.html', {'src':src})
        elif selected_option == 'NM3':
            src="https://lookerstudio.google.com/embed/reporting/b9ee496c-dd50-4d91-baf4-0c5f6769c84a/page/p_zn918rlshd"
            return render(request, 'nmiframe.html', {'src':src})
        elif selected_option == 'NM4':
            src="https://lookerstudio.google.com/embed/reporting/e89c7546-11e7-4e0a-9700-b49dc74494a0/page/bZt0D"
            return render(request, 'nmiframe.html', {'src':src})
    return render(request,"edutech.html")

@login_required
def finance(request):
    return render(request, 'finance.html')

@login_required
@group_required(groups=['trainer'])
def trainer(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Get JSON data from request
        image_data = data.get('image')
        timestamp = data.get('timestamp')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        description = data.get('description')

        # Decode the base64 image
        image_data = image_data.split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        
        # Save the image to a Django ImageField
        image_file = ContentFile(base64.b64decode(image_data), name=f'{timestamp}.jpg')

        # Create and save the CapturedPhoto object
        captured_photo = CapturedPhoto(
            user=request.user,
            image=image_file,
            timestamp=datetime.fromisoformat(timestamp),
            latitude=latitude,
            longitude=longitude,
            description=description
        )
        captured_photo.save()

        return redirect('logout')

    return render(request, 'trainer_form.html')

import csv

@login_required
@group_required(groups=['coordinator'])
def filter_photos(request):
    trainer_group = Group.objects.get(name='trainer')
    trainer_users = User.objects.filter(groups=trainer_group)
    photos = CapturedPhoto.objects.none()  # Initialize as empty queryset

    selected_user = 'all'
    selected_date = ''
    export = False

    if request.method == "POST":
        selected_user = request.POST.get('user', 'all')
        selected_date = request.POST.get('date', '')

        if selected_user == 'all':
            photos = CapturedPhoto.objects.all()
        else:
            photos = CapturedPhoto.objects.filter(user_id=selected_user)

        if selected_date:
            try:
                # Convert string to date object
                selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
                photos = photos.filter(timestamp__date=selected_date_obj)
            except ValueError:
                # Handle invalid date input
                pass

        if 'export' in request.POST:
            export = True 

    context = {
        'users': trainer_users,
        'photos': photos,
        'selected_user': selected_user,
        'selected_date': selected_date,
    }

    if export:
        return export_photos_to_csv(photos)
    
    return render(request, 'filter_photos.html', context)


def export_photos_to_csv(photos):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_photos.csv"'

    # Write CSV headers
    writer = csv.writer(response)
    writer.writerow(['Username', 'Timestamp', 'Description', 'Latitude', 'Longitude'])

    # Write CSV rows
    for photo in photos:
        writer.writerow([photo.user.username, photo.timestamp, photo.description, photo.latitude, photo.longitude])

    return response