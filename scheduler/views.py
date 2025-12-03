from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Owner, Veterinarian, Appointment
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirect based on role
            if user.is_superuser:
                return redirect('dashboard')

            elif hasattr(user, 'owner'):
                return redirect('user_dashboard')

            elif hasattr(user, 'veterinarian'):
                return redirect('doctor_dashboard')

            else:
                messages.error(request, "No dashboard assigned for this user.")
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'scheduler/login.html')


# -------------------------
# LOGOUT VIEW
# -------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------
# MAIN DASHBOARD ROUTER
# -------------------------
@login_required
def dashboard(request):
    # Owner → User Dashboard
    if hasattr(request.user, 'owner'):
        return redirect('user_dashboard')

    # Doctor → Doctor Dashboard
    elif hasattr(request.user, 'veterinarian'):
        return redirect('doctor_dashboard')

    # Admin → Admin Dashboard
    return render(request, 'scheduler/admin_dashboard.html')



# -------------------------
# USER DASHBOARD
# -------------------------
@login_required
def user_dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'scheduler/user_dashboard.html', {
        'appointments': appointments
    })


# -------------------------
# DOCTOR DASHBOARD
# -------------------------
@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor__user=request.user)
    return render(request, 'scheduler/doctor_dashboard.html', {
        'appointments': appointments
    })


# -------------------------
# APPOINTMENT LIST
# -------------------------
@login_required
def appointment_list(request):
    if hasattr(request.user, 'veterinarian'):
        appointments = Appointment.objects.filter(doctor__user=request.user)

    elif hasattr(request.user, 'owner'):
        appointments = Appointment.objects.filter(user=request.user)

    else:
        appointments = Appointment.objects.all()

    return render(request, 'scheduler/appointment_list.html', {
        'appointments': appointments
    })


# -------------------------
# PROFILE VIEW
# -------------------------
@login_required
def profile_view(request):
    context = {}

    if hasattr(request.user, 'owner'):
        context['profile_type'] = 'User'
        context['profile'] = request.user.owner

    elif hasattr(request.user, 'veterinarian'):
        context['profile_type'] = 'Doctor'
        context['profile'] = request.user.veterinarian

    else:
        context['profile_type'] = 'Admin'
        context['profile'] = request.user

    return render(request, 'scheduler/profile.html', context)


# -------------------------
# EMAIL REMINDERS
# -------------------------
def send_reminders():
    today = timezone.now().date()
    appointments = Appointment.objects.filter(date=today, reminder_sent=False)

    for a in appointments:
        if a.user and a.user.email:
            send_mail(
                subject=f"Appointment Reminder: {a.date}",
                message=f"Dear {a.user.username}, your appointment for {a.pet.name} "
                        f"with Dr. {a.doctor.name} is scheduled at {a.time}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[a.user.email],
            )
        a.reminder_sent = True
        a.save()
