from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import UserRegisterForm, UserLoginForm,VehicleListingForm
from users.models import UserProfile,VehicleListing

def home(request):
    approved_listings = VehicleListing.objects.filter(is_approved=True)
    context = {
        'approved_listings': approved_listings
    }
    return render(request, 'users/home.html', context)

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user, mobile_number=form.cleaned_data.get('mobile_number'), user_type=form.cleaned_data.get('user_type'))
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
def owner_home(request):
    approved_listings = VehicleListing.objects.filter(is_approved=True)
    context = {
        'approved_listings': approved_listings
    }
    return render(request, 'users/owner_home.html', context)

@login_required
def sell_vehicle(request):
    if request.method == 'POST':
        form = VehicleListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('home')  # Redirect to home page after successful submission
    else:
        form = VehicleListingForm()
    
    return render(request, 'users/sell_vehicle.html', {'form': form})