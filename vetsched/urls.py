from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduler.urls')),
]


def redirect_to_dashboard(request):
    return redirect('dashboard')   # or 'doctor_dashboard' if you prefer

urlpatterns = [
    path('admin/', admin.site.urls),        
    path('', include('scheduler.urls')),
   # Load clinic URLs FIRST
    path('home/', redirect_to_dashboard),   # Optional redirect
]
