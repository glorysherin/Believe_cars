# users/urls.py
from django.urls import path
from .views import user_views, owner_views,landing_views

urlpatterns = [
    path('home', user_views.home, name='home'),
    path('register/', user_views.user_register, name='user-register'),
    path('login/', user_views.user_login, name='user-login'),
    path('logout/', user_views.user_logout, name='user-logout'),
    path('owner/login/', owner_views.owner_login, name='owner-login'),
    path('owner/home/', user_views.owner_home, name='owner-home'),
    path('owner/extract/', owner_views.extract_user_details, name='extract-user-details'),
    path('sell-vehicle/', user_views.sell_vehicle, name='sell-vehicle'),
    path('owner/view-approvals/', owner_views.view_approvals, name='view-approvals'),
    path('owner/approve-listing/<int:listing_id>/', owner_views.approve_listing, name='approve-listing'),

    path('owner/reject-listing/<int:listing_id>/', owner_views.reject_listing, name='reject-listing'),
    path('vehicle/<int:listing_id>/', user_views.view_vehicle, name='view-vehicle'),
    path('owner/view_vehicle/<int:listing_id>/', owner_views.view_vehicle, name='owner-view-vehicle'),
 path('owner/add-details/<int:listing_id>/', owner_views.add_details, name='add-details'),  # New path for add details
 path('',landing_views.landing_page,name='landing')
]

#  path('sell_vehicle/', user_views.sell_vehicle, name='sell_vehicle'),
    # path('view_vehicle/<int:vehicle_id>/', owner_views .view_vehicle, name='view_vehicle'),

