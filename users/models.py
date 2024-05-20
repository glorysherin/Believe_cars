# users/models.py

from django.contrib.auth.models import User
from django.db import models

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
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    kms_driven = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    pitching_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='vehicle_images/')
    is_approved = models.BooleanField(default=False)
    star_rating = models.IntegerField(null=True, blank=True)  # New field for star ratings
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"
    
    @staticmethod
    def get_pending_approvals():
        return VehicleListing.objects.filter(is_approved=False)
