from django.contrib import admin
from .models import Owner, Pet, Veterinarian, Appointment

# ----------------- Appointment Admin -----------------
class AppointmentAdmin(admin.ModelAdmin):
    # Columns to display in dashboard table
    list_display = (
        'pet_name',
        'owner_name',
        'owner_phone',
        'doctor_name',
        'date',
        'time',
        'status'
    )

    # Filters on right side → use 'doctor' (not 'vet')
    list_filter = ('status', 'date', 'doctor')

    # Search bar
    search_fields = (
        'pet__name',
        'pet__owner__name',
        'pet__owner__phone',
        'doctor__username'  # 'doctor' is a ForeignKey to User
    )

    # ---------- Custom Column Functions ----------
    def pet_name(self, obj):
        return obj.pet.name

    def owner_name(self, obj):
        return obj.pet.owner.name

    def owner_phone(self, obj):
        return obj.pet.owner.phone

    def doctor_name(self, obj):
        return obj.doctor.username

    # Column names
    pet_name.short_description = "Pet"
    owner_name.short_description = "Owner"
    owner_phone.short_description = "Phone"
    doctor_name.short_description = "Doctor / Veterinarian"

# ----------------- Register Models -----------------
admin.site.register(Owner)
admin.site.register(Pet)
admin.site.register(Veterinarian)
admin.site.register(Appointment, AppointmentAdmin)
