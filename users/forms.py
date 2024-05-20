# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,VehicleListing

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
    
    
class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = ['brand', 'model', 'year', 'kms_driven', 'fuel_type', 'location', 'pitching_price', 'product_image']