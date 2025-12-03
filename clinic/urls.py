from django.urls import path
from . import views

urlpatterns = [
    # Dashboard URLs
    path('', views.main_dashboard, name='dashboard'),
    path('dashboard/', views.main_dashboard, name='dashboard'),

    # User dashboard URL
    path('user/', views.user_dashboard, name='user_dashboard'),

    # Appointments URL
    path('appointments/', views.appointments, name='appointments'),

    # Profile URL
    path('profile/', views.profile, name='profile'),  # ✅ Added
]
