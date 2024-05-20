from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Import redirect function
from users.views.owner_views import owner_login  # Import the owner login view
from django.conf import settings
from django.conf.urls.static import static


# Define redirect_to_owner_login function first
def redirect_to_owner_login(request):
    return redirect('owner-login')  # Redirect to the 'owner-login' URL name defined in users/urls.py

# Define urlpatterns after defining redirect_to_owner_login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('users.urls')),  # Include users app URLs for the root path
    path('accounts/login/', redirect_to_owner_login),  # Redirect accounts/login/ to owner login
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)