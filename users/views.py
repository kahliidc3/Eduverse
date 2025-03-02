from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomSignupForm, CustomLoginForm
from gamification.models import Point, Achievement, UserAchievement

# Create your views here.

@login_required
def dashboard(request):
    # Get total points
    total_points = Point.objects.filter(user=request.user).aggregate(
        total=models.Sum('points'))['total'] or 0
    
    # Get recent achievements
    recent_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-achieved_at')[:3]
    
    return render(request, 'users/dashboard.html', {
        'total_points': total_points,
        'recent_achievements': recent_achievements,
    })

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    # Get user's points
    total_points = Point.objects.filter(user=request.user).aggregate(
        total=models.Sum('points'))['total'] or 0
    
    # Get user's achievements
    achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-achieved_at')
    
    context = {
        'form': form,
        'total_points': total_points,
        'achievements': achievements,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {
        'form': form,
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Welcome to EduVerse! Your account has been created successfully.'))
            return redirect('home')
    else:
        form = CustomSignupForm()
    
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                messages.success(request, _('Welcome back!'))
                
                # Redirect to next URL if provided, otherwise go to home
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, _('Invalid email or password.'))
    else:
        form = CustomLoginForm()
    
    return render(request, 'account/login.html', {'form': form})
