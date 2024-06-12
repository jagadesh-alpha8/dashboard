from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def handler404(request, exception):
    return render(request, 'error.html', status=404)

# Create your views here.
def user_login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Invalid Username or Password')
            return render(request, 'login.html')
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


def finance(request):
    return render(request, 'finance.html')