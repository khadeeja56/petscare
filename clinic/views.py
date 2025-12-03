from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm

# --------------------------
# LOGIN / LOGOUT
# --------------------------
def login_view(request):
    if request.user.is_authenticated:
        # Already logged in → redirect based on role
        if request.user.is_superuser or request.user.is_staff:
            return redirect('dashboard')      # Admin dashboard
        else:
            return redirect('user_dashboard') # Regular user dashboard

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# --------------------------
# DASHBOARDS
# --------------------------
@login_required
def main_dashboard(request):
    user = request.user

    # Check roles
    is_doctor = user.groups.filter(name='Doctor').exists()
    is_patient = user.groups.filter(name='Patient').exists()
    is_admin = user.is_staff

    context = {
        'is_doctor': is_doctor,
        'is_patient': is_patient,
        'is_admin': is_admin,
    }

    return render(request, 'dashboard.html', context)


@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# --------------------------
# PROFILE
# --------------------------
@login_required
def profile(request):
    return render(request, 'profile.html')


# --------------------------
# HOME / REDIRECT
# --------------------------
@login_required
def home(request):
    return redirect('appointment_list')


# --------------------------
# APPOINTMENTS CRUD
# --------------------------
@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})


@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})


@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointment_form.html', {'form': form})


@login_required
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'appointment_confirm_delete.html', {'appointment': appointment})
