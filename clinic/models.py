from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# -------------------------
# Patient Model (Merged)
# -------------------------
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    contact = models.CharField(max_length=50, blank=True, null=True)  # optional field from your first model

    def __str__(self):
        return self.name


# -------------------------
# Appointment Model
# -------------------------
class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.username} on {self.date}"
email = models.EmailField(default="example@example.com")
