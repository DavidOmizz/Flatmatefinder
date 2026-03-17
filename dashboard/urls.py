from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('requests/', views.request_list, name='requests'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('listings/', views.listings_overview, name='listings'),
    path('users/', views.users_overview, name='users'),
]
