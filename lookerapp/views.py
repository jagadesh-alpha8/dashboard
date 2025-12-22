from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

import base64
import io
from datetime import datetime
from PIL import Image
from django.core.files.base import ContentFile
from .models import CapturedPhoto
import json
from dateutil.parser import parse as parse_date

from django.contrib.auth.models import User, Group
from django.utils.timezone import make_aware
from .decorator import group_required

def handler404(request, exception):
    return render(request, 'error.html', status=404)

def user_login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='nm').exists():
            return redirect('edutech')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.groups.filter(name='nm').exists():
                return redirect('edutech')
            elif request.user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def contact(request):
    return render(request, 'error.html')

@login_required
@group_required(groups=['trainer','coordinator','hcl'])
def home(request):
    if request.method == 'POST':
        selected_option = request.POST.get('bname')
        if selected_option == 'edu1':
            return render(request, 'edu.html')
    return render(request, 'home.html')

@login_required
@group_required(groups=['coordinator','nm'])
def edu(request):
        if request.method == 'POST':
            selected_option = request.POST.get('type')
            if selected_option == 'NM':
                return render(request, "edutech.html")
            elif selected_option == 'train':
                return render(request, "error.html")
            elif selected_option == 'value':
                return render(request, "error.html")


@login_required
@group_required(groups=['coordinator','nm'])
def edutech(request):
    if request.method == 'POST':
        selected_option = request.POST.get('nm')
        if selected_option == 'NM1':
            src = "https://lookerstudio.google.com/embed/reporting/7ca9ee3b-57ee-433f-a0f5-bad9570789af/page/FPr1D"
            return render(request, 'nmiframe.html', {'src': src})
        elif selected_option == 'NM2':
            src = "https://lookerstudio.google.com/embed/reporting/06495847-6471-446d-87df-251f86984224/page/FPr1D"
            return render(request, 'nmiframe.html', {'src': src})
        elif selected_option == 'NM3':
            src = "https://lookerstudio.google.com/embed/reporting/b2918892-9a34-48ec-83b4-7b084bbbfc93/page/FPr1D"
            return render(request, 'nmiframe.html', {'src': src})
        elif selected_option == 'NM4':
            src = "https://lookerstudio.google.com/embed/reporting/06296e56-68a2-45a3-b603-22b13ef64853/page/FPr1D"
            return render(request, 'nmiframe.html', {'src': src})
        elif selected_option == 'NM5':
            src = "https://lookerstudio.google.com/embed/reporting/4a51655c-ad20-4422-8791-b6be75d424a7/page/FPr1D"
            return render(request, 'nmiframe.html', {'src': src})
        elif selected_option == 'NM6':
            src = "https://lookerstudio.google.com/embed/reporting/a264b443-9de8-42ea-8172-5def68949882/page/FPr1D"
            return render(request, 'nmiframe.html', {'src': src})
        elif selected_option == 'NM7':
            src = "https://lookerstudio.google.com/embed/reporting/67d94127-6c59-4a9f-b259-19d96936d5e1/page/p_atllecikyd"
            return render(request, 'nmiframe.html', {'src': src})
        
        
    return render(request, "edutech.html")



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
        place_name = data.get('place_name')
        print(place_name)

        # Decode the base64 image
        image_data = image_data.split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Save the image to a Django ImageField
        image_file = ContentFile(base64.b64decode(image_data), name=f'{timestamp}.jpg')

        # Parse the ISO 8601 timestamp with timezone information
        timestamp_dt = parse_date(timestamp)

        # Create and save the CapturedPhoto object
        captured_photo = CapturedPhoto(
            user=request.user,
            image=image_file,
            timestamp=timestamp_dt,
            latitude=latitude,
            longitude=longitude,
            description=description,
            place_name=place_name
        )
        captured_photo.save()

        return redirect('home')

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
    writer.writerow(['Username', 'Timestamp', 'Description','place_name', 'Latitude', 'Longitude'])

    # Write CSV rows
    for photo in photos:
        writer.writerow([photo.user.username, photo.timestamp, photo.description,photo.place_name, photo.latitude, photo.longitude])

    return response



def csrf_failure(request, reason=""):
    # return render(request, 'error.html', {'reason': reason})
    return redirect('login')




# import pandas as pd

# df = pd.read_excel(r"C:\Users\ingag\OneDrive\Desktop\Login ID's.xlsx")

# from django.contrib.auth.models import User, Group

# # Ensure the group exists
# group = Group.objects.get(name='trainer')

# for index, row in df.iterrows():
#     username = row['user_id']
    
#     if not User.objects.filter(username=username).exists():
#         user = User.objects.create_user(
#             username=username,
#             password=str(row['password']),  # Convert password to string
#             first_name=row['first_name'],
#             last_name=row['last_name'],
#             email=row['email']
#         )
#         # Add the user to the group
#         user.groups.add(group)
#     else:
#         print(f"User {username} already exists.")
