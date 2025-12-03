from django.db import models
from django.contrib.auth.models import User

# ----------------- Owner Model -----------------
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

# ----------------- Pet Model -----------------
class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.owner.name})"

# ----------------- Veterinarian (Doctor) Model -----------------
class Veterinarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # doctor login
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# ----------------- Appointment Model -----------------
class Appointment(models.Model):
    # patient → user account
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)

    # pet → linked to owner
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)

    # doctor → veterinarian
    doctor = models.ForeignKey(Veterinarian, on_delete=models.CASCADE, related_name='doctor_appointments', null=True, blank=True)

    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    reminder_sent = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        pet_name = self.pet.name if self.pet else "Unknown Pet"
        user_name = self.user.username if self.user else "Unknown User"
        return f"{pet_name} for {user_name} on {self.date}"

    # Helper method for admin/templates
    def doctor_name(self):
        return self.doctor.name if self.doctor else "N/A"
