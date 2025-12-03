from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, Pet, Veterinarian

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Veterinarian.objects.all(),
        required=True
    )

    pet = forms.ModelChoiceField(
        queryset=Pet.objects.all(),
        required=True
    )

    class Meta:
        model = Appointment
        fields = ['pet', 'doctor', 'date', 'time', 'status', 'reason', 'notes']
