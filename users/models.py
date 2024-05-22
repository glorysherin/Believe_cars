# users/models.py

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username
    

class VehicleListing(models.Model):
    seller_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    kms_driven = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    pitching_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='vehicle_images/')
    additional_image1 = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    additional_image2 = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    additional_image3 = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    additional_image4 = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    star_rating = models.IntegerField(null=True, blank=True)
    condition_description = models.TextField(null=True, blank=True)
    owner_review = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    registration_year = models.IntegerField()  # Remove default value
    transmission = models.CharField(max_length=50)  # Remove default value
    num_owners = models.IntegerField()  # Remove default value
    insurance_type = models.CharField(max_length=100)  # Remove default value
    insurance_validity = models.DateField()
    rto = models.CharField(max_length=100)  # Remove default value
    full_details = models.FileField(upload_to='full_details/', null=True, blank=True)  # New field


    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"

    @staticmethod
    def get_pending_approvals():
        return VehicleListing.objects.filter(is_approved=False)

class CarSpecification(models.Model):
    vehicle_listing = models.OneToOneField(VehicleListing, on_delete=models.CASCADE, related_name='car_spec')
    mileage_arai = models.CharField(max_length=50)
    boot_space = models.CharField(max_length=50)
    ground_clearance = models.CharField(max_length=50)
    seating_capacity = models.CharField(max_length=50)
    fuel_tank_capacity = models.CharField(max_length=50)
    displacement = models.CharField(max_length=50)

    def __str__(self):
        return f"Specifications for {self.vehicle_listing.brand} {self.vehicle_listing.model} - {self.vehicle_listing.year}"

class InspectionReport(models.Model):
    vehicle_listing = models.OneToOneField(VehicleListing, on_delete=models.CASCADE, related_name='inspection_report')
    engine_peripherals = models.TextField()
    drivetrain = models.TextField()
    body_structure_chassis = models.TextField()
    exterior = models.TextField()
    interior = models.TextField()
    mechanical = models.TextField()
    wheels_tyres = models.TextField()


    def __str__(self):
        return f"Inspection Report for {self.vehicle_listing.brand} {self.vehicle_listing.model} - {self.vehicle_listing.year}"