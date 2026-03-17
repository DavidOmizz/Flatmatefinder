from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listing_list, name='list'),
    path('listings/create/', views.listing_create, name='create'),
    path('listings/<int:pk>/', views.listing_detail, name='detail'),
    path('listings/<int:pk>/edit/', views.listing_edit, name='edit'),
    path('listings/<int:pk>/delete/', views.listing_delete, name='delete'),
    path('listings/<int:pk>/save/', views.toggle_save, name='save'),
    path('my-requests/', views.my_requests, name='requests'),
    path('saved/', views.saved_listings, name='saved'),
]
