# users/views/owner_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from users.forms import OwnerLoginForm,VehicleListingForm,CarSpecificationForm, InspectionReportForm
import openpyxl
from django.http import HttpResponse
from users.models import UserProfile,CarSpecification  ,InspectionReport
from django.db import transaction

import openpyxl
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from users.models import UserProfile,VehicleListing

def owner_login(request):
    # Check if any superuser exists
    if not User.objects.filter(is_superuser=True).exists():
        error_message = "No superuser exists. Please create a superuser first."
        return render(request, 'users/owner_login.html', {'error_message': error_message})

    if request.method == 'POST':
        form = OwnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                # Redirect to owner home page after successful login
                return redirect('owner-home')  # Redirect to 'owner-home' URL
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = OwnerLoginForm()
    
    return render(request, 'users/owner_login.html', {'form': form})



# users/views/owner_views.py


def is_owner(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_owner)
def extract_user_details(request):
    # Query all users who are not superusers
    users = User.objects.exclude(is_superuser=True)
    
    # Create Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "User Details"

    # Define headers
    ws.append(['Username', 'Email', 'Phone Number', 'User Type'])

    # Iterate over users and populate data
    for user in users:
        profile = UserProfile.objects.get(user=user)
        ws.append([user.username, user.email, profile.mobile_number, profile.get_user_type_display()])

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openpyxl.sheet')
    response['Content-Disposition'] = 'attachment; filename="user_details.xlsx"'

    # Save workbook to response
    wb.save(response)

    return response



@user_passes_test(is_owner)
def view_approvals(request):
    pending_listings = VehicleListing.get_pending_approvals()
    context = {
        'pending_listings': pending_listings
    }
    return render(request, 'users/view_approvals.html', context)


@user_passes_test(is_owner)
def approve_listing(request, listing_id):
    listing = get_object_or_404(VehicleListing, id=listing_id)
    if request.method == 'POST':
        star_rating = request.POST.get('star_rating')
        owner_review = request.POST.get('owner_review')
        listing.star_rating = star_rating
        listing.owner_review = owner_review
        listing.is_approved = True
        listing.save()
        # Optionally, you can add a success message here
        # return redirect('view-approvals')
        return redirect('owner-home')  # Redirect to 'owner-home' URL

    return render(request, 'users/approve_listing.html', {'listing': listing})

@user_passes_test(is_owner)
def reject_listing(request, listing_id):
    listing = get_object_or_404(VehicleListing, id=listing_id)
    listing.delete()
    messages.success(request, 'Listing has been rejected and deleted.')
    return redirect('view-approvals')

@user_passes_test(is_owner)
def add_details(request, listing_id):
    listing = get_object_or_404(VehicleListing, pk=listing_id)
    
    try:
        car_spec = listing.car_spec
    except CarSpecification.DoesNotExist:
        car_spec = None
    
    try:
        inspection_report = listing.inspection_report
    except InspectionReport.DoesNotExist:
        inspection_report = None

    if request.method == 'POST':
        vehicle_form = VehicleListingForm(request.POST, request.FILES, instance=listing)
        car_spec_form = CarSpecificationForm(request.POST, instance=car_spec)
        inspection_report_form = InspectionReportForm(request.POST, instance=inspection_report)
        
        if vehicle_form.is_valid() and car_spec_form.is_valid() and inspection_report_form.is_valid():
            try:
                with transaction.atomic():
                    vehicle_form.save()
                    
                    car_spec = car_spec_form.save(commit=False)
                    car_spec.vehicle_listing = listing
                    car_spec.save()
                    
                    inspection_report = inspection_report_form.save(commit=False)
                    inspection_report.vehicle_listing = listing
                    inspection_report.save()

                    messages.success(request, 'Details added successfully.')
                    # Redirect to approve listing page with the listing_id
                    return redirect('approve-listing', listing_id=listing.id)
            except Exception as e:
                messages.error(request, f'Error occurred: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        vehicle_form = VehicleListingForm(instance=listing)
        car_spec_form = CarSpecificationForm(instance=car_spec)
        inspection_report_form = InspectionReportForm(instance=inspection_report)

    context = {
        'listing': listing,
        'vehicle_form': vehicle_form,
        'car_spec_form': car_spec_form,
        'inspection_report_form': inspection_report_form,
    }

    return render(request, 'users/add_details.html', context)

# View to display approved listings on home page
# View to display approved listings on home page
def home(request):
    approved_listings = VehicleListing.objects.filter(is_approved=True).order_by('-uploaded_at')
    context = {
        'approved_listings': approved_listings
    }
    return render(request, 'users/owner_home.html', context)


@user_passes_test(is_owner)
def view_vehicle(request, listing_id):
    listing = get_object_or_404(VehicleListing, id=listing_id)
    return render(request, 'users/view_vehicle.html', {'listing': listing})
# def view_vehicle(request, listing_id):
#     listing = get_object_or_404(VehicleListing, id=listing_id)
#     context = {
#         'listing': listing
#     }
#     return render(request, 'users/view_vehicle.html', context)
