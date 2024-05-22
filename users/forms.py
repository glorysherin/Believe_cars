# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,VehicleListing,CarSpecification, InspectionReport, VehicleListing

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'user_type', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class OwnerLoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()
            if user is None or not user.check_password(password):
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data
  # forms.py

class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = ['seller_name', 'mobile_number', 'brand', 'model', 'year', 'product_image', 
                  'additional_image1', 'additional_image2', 'additional_image3', 'additional_image4', 
                   # New field
                  'pitching_price', 'kms_driven', 'fuel_type', 'location', 'condition_description',
                  'registration_year', 'transmission', 'num_owners', 'insurance_type', 
                  'insurance_validity', 'rto','full_details']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example: Add placeholders or additional attributes to form fields
        self.fields['registration_year'].widget.attrs['placeholder'] = 'YYYY'
        self.fields['kms_driven'].widget.attrs['placeholder'] = 'Enter kilometers'
    
    def clean(self):
        cleaned_data = super().clean()
        additional_image1 = cleaned_data.get("additional_image1")
        additional_image2 = cleaned_data.get("additional_image2")
        additional_image3 = cleaned_data.get("additional_image3")
        additional_image4 = cleaned_data.get("additional_image4")

        # Validate that all four additional images are uploaded
        if not (additional_image1 and additional_image2 and additional_image3 and additional_image4):
            raise forms.ValidationError("All four additional images must be uploaded.")

        # Example: Add more validation logic as needed
        pitching_price = cleaned_data.get("pitching_price")
        if pitching_price <= 0:
            raise forms.ValidationError("Pitching price must be greater than zero.")

        return cleaned_data
    
    
class CarSpecificationForm(forms.ModelForm):
    class Meta:
        model = CarSpecification
        fields = ['mileage_arai', 'boot_space', 'ground_clearance', 'seating_capacity',
                  'fuel_tank_capacity', 'displacement']

class InspectionReportForm(forms.ModelForm):
    ENGINE_PERIPHERALS_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    DRIVETRAIN_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    # Add more choices as needed

    engine_peripherals = forms.ChoiceField(
        choices=ENGINE_PERIPHERALS_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'engine-peripherals'})
    )
    drivetrain = forms.ChoiceField(
        choices=DRIVETRAIN_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'drivetrain'})
    )
    # Add more fields with radio choices

    class Meta:
        model = InspectionReport
        fields = ['engine_peripherals', 'drivetrain', 'body_structure_chassis',
                  'exterior', 'interior', 'mechanical', 'wheels_tyres']