from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
import random

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Email already registered!'})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already taken!'})

        if password != confirm:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match!'})

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            role=role,
            password=password
        )
        user.save()
        return redirect('login')

    return render(request, 'accounts/register.html')

def set_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        
        if password == confirm:
            user_id = request.session.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'accounts/set_password.html', {'error': 'Passwords do not match'})
    
    return render(request, 'accounts/set_password.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')