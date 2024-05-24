# users/views/owner_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from users.forms import OwnerLoginForm,VehicleListingForm
import openpyxl
from django.http import HttpResponse
from users.models import UserProfile
from django.db import transaction
from users.forms import CarDetailsForm,ApprovalForm
from django.http import HttpResponse, Http404
from users.forms import CarDetailsForm
from users.models import CarDetails
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


# @user_passes_test(is_owner)
# def approve_listing(request, listing_id):
#     listing = get_object_or_404(VehicleListing, id=listing_id)
#     if request.method == 'POST':
#         star_rating = request.POST.get('star_rating')
#         owner_review = request.POST.get('owner_review')
#         listing.star_rating = star_rating
#         listing.owner_review = owner_review
#         listing.is_approved = True
#         listing.save()
#         # Optionally, you can add a success message here
#         # return redirect('view-approvals')
#         return redirect('owner-home')  # Redirect to 'owner-home' URL

#     return render(request, 'users/approve_listing.html', {'listing': listing})

@user_passes_test(is_owner)
def reject_listing(request, listing_id):
    listing = get_object_or_404(VehicleListing, id=listing_id)
    listing.delete()
    messages.success(request, 'Listing has been rejected and deleted.')
    return redirect('view-approvals')



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

@user_passes_test(is_owner)
def add_details(request, listing_id):
    listing = get_object_or_404(VehicleListing, id=listing_id)

    if request.method == 'POST':
        form = CarDetailsForm(request.POST)
        if form.is_valid():
            car_details = form.save(commit=False)
            car_details.vehicle_listing = listing
            car_details.star_rating = request.POST.get('star_rating')  # Add star rating
            car_details.owner_review = request.POST.get('owner_review')  # Add owner review
            car_details.save()
            listing.is_approved = True  # Update the listing approval status if needed
            listing.save()
            return redirect('view-approvals')  # Redirect to approvals page after submission
    else:
        form = CarDetailsForm()

    context = {
        'form': form,
        'listing': listing
    }
    return render(request, 'users/add_details.html', context)
# @user_passes_test(is_owner)
# def success(request):
#     return render(request, 'users/success.html')

@user_passes_test(is_owner)
def submit_details(request, listing_id):
    # Fetch the listing object based on listing_id
    listing = get_object_or_404(VehicleListing, id=listing_id)

    if request.method == 'POST':
        # Process form data
        listing.mileage = request.POST.get('mileage')
        listing.boot_space = request.POST.get('boot_space')
        listing.ground_clearance = request.POST.get('ground_clearance')
        listing.seating_capacity = request.POST.get('seating_capacity')
        listing.fuel_tank_capacity = request.POST.get('fuel_tank_capacity')
        listing.displacement = request.POST.get('displacement')
        
        listing.engine_peripherals = request.POST.get('engine_peripherals')
        listing.drivetrain = request.POST.get('drivetrain')
        listing.body_structure = request.POST.get('body_structure')
        listing.exterior = request.POST.get('exterior')
        listing.interior = request.POST.get('interior')
        listing.mechanical = request.POST.get('mechanical')
        listing.wheels_tyres = request.POST.get('wheels_tyres')
        
        # Save the updated listing object
        listing.save()

        # Redirect to a success page or back to the view approvals page
        return redirect('view-approvals')

    # Render the add details form template for GET requests
    context = {
        'listing': listing,
    }
    return render(request, 'add_details.html', context)




def car_details_view(request, car_details_id):
    car_details = get_object_or_404(CarDetails, id=car_details_id)
    return render(request, 'users/details.html', {'car_details': car_details})
# def save_details(request, listing_id):
#     listing = get_object_or_404(Listing, pk=listing_id)
    
#     if request.method == 'POST':
#         # Extract data from POST request
#         mileage = request.POST.get('mileage')
#         boot_space = request.POST.get('boot_space')
#         ground_clearance = request.POST.get('ground_clearance')
#         seating_capacity = request.POST.get('seating_capacity')
#         fuel_tank_capacity = request.POST.get('fuel_tank_capacity')
#         displacement = request.POST.get('displacement')
        
#         engine_peripherals = request.POST.get('engine_peripherals')
#         drivetrain = request.POST.get('drivetrain')
#         body_structure = request.POST.get('body_structure')
#         exterior = request.POST.get('exterior')
#         interior = request.POST.get('interior')
#         mechanical = request.POST.get('mechanical')
#         wheels_tyres = request.POST.get('wheels_tyres')
        
#         # Save the details in your model (for example, SavedDetails model)
#         saved_details = SavedDetails.objects.create(
#             listing=listing,
#             mileage=mileage,
#             boot_space=boot_space,
#             ground_clearance=ground_clearance,
#             seating_capacity=seating_capacity,
#             fuel_tank_capacity=fuel_tank_capacity,
#             displacement=displacement,
#             engine_peripherals=engine_peripherals,
#             drivetrain=drivetrain,
#             body_structure=body_structure,
#             exterior=exterior,
#             interior=interior,
#             mechanical=mechanical,
#             wheels_tyres=wheels_tyres
#         )
        
#         # Redirect to the approve listing page
#         return redirect('approve-listing')
    
#     # If not POST request, render the form
#     context = {
#         'listing': listing,
#     }
#     return render(request, 'add_details.html', context)

# def approve_listing(request):
#     # Fetch all saved details to display in approve-listing.html
#     saved_details = SavedDetails.objects.all()  # Query as per your SavedDetails model
    
#     context = {
#         'saved_details': saved_details,
#     }
#     return render(request, 'approve-listing.html', context)
