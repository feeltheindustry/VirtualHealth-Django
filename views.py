# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .forms import UserCreationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html', {'user': request.user})
    else:
        return redirect('login')

def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("You do not have access to this page.")
    return render(request, 'accounts/doctor_dashboard.html')

def patient_dashboard(request):
    if request.user.role != 'patient':
        return HttpResponseForbidden("You do not have access to this page.")
    return render(request, 'accounts/patient_dashboard.html')
