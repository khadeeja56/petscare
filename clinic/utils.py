from django.core.mail import send_mail

def send_appointment_email(appointment, owner_email):
    subject = f"Appointment Confirmation for {appointment.pet_name}"
    message = f"Hello {appointment.owner_name},\nYour appointment for {appointment.pet_name} is scheduled on {appointment.date}."
    recipient_list = [owner_email]
    send_mail(subject, message, None, recipient_list)
from twilio.rest import Client
from django.conf import settings

def send_appointment_sms(appointment, owner_phone):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = f"Hello {appointment.owner_name}, your appointment for {appointment.pet_name} is on {appointment.date}."
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=owner_phone
    )
