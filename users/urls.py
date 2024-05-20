# users/urls.py

from django.urls import path
from .views import user_views, owner_views

urlpatterns = [
    path('', user_views.home, name='home'),
    path('register/', user_views.user_register, name='user-register'),
    path('login/', user_views.user_login, name='user-login'),
    path('logout/', user_views.user_logout, name='user-logout'),
    path('owner/login/', owner_views.owner_login, name='owner-login'),
    path('owner/home/', user_views.owner_home, name='owner-home'),  # Define 'owner-home' URL for owner/superuser
    path('owner/extract/', owner_views.extract_user_details, name='extract-user-details'),  # Add URL for extracting user details
    # URL for selling vehicle form
    path('sell-vehicle/', user_views.sell_vehicle, name='sell-vehicle'),

    # URL for viewing pending approvals
    path('owner/view-approvals/', owner_views.view_approvals, name='view-approvals'),

   path('owner/approve-listing/<int:listing_id>/', owner_views.approve_listing, name='approve-listing'),
    path('owner/reject-listing/<int:listing_id>/', owner_views.reject_listing, name='reject-listing'),
]