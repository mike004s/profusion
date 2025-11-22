from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirmpassword = request.POST.get('re-pass', '').strip()
        
        if not all([username, email, password, confirmpassword]):
            messages.error(request, "All fields are required")
            return render(request, 'signup.html')
        
        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')
        
        if len(username) < 8:
            messages.error(request, "Username must be at least 8 characters long")
            return render(request, 'signup.html')
            
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, f'{username} created successfully')
        return redirect('login')
        
    return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

    
def Logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


@login_required(login_url='/accounts/login/')
def profile_view(request):
    """View user profile (GET only)"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='/accounts/login/')
def profile_edit(request):
    """Edit user profile (POST)"""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        avatar = request.FILES.get('avatar')

        # Update user fields
        if name:
            request.user.username = name
        if email:
            request.user.email = email
        request.user.save()

        # Update profile avatar
        if avatar:
            profile.avatar = avatar
            profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile_view')
    
    return render(request, 'profile_edit.html', {'profile': profile})