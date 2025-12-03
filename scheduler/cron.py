from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import os

# -------------------- Twilio setup --------------------
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_FROM = os.environ.get('TWILIO_FROM')

def send_sms(to, body):
    """
    Sends SMS using Twilio if credentials and phone number exist
    """
    if to and TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(body=body, from_=TWILIO_FROM, to=to)

# -------------------- Reminder logic --------------------
def send_reminders_cron():
    """
    Sends email and optional SMS reminders for appointments happening
    within the next hour and not yet marked as reminder_sent.
    """
    now = timezone.now()
    upcoming_date = now.date()
    one_hour_from_now = (now + timedelta(hours=1)).time()

    # Find appointments on the same date with reminder_sent=False
    appts = Appointment.objects.filter(
        date=upcoming_date,
        reminder_sent=False
    )

    for appt in appts:
        appt_time = appt.time
        if now.time() <= appt_time <= one_hour_from_now:
            # ---------------- Email ----------------
            subject = 'Appointment Reminder from Vetsched'
            body = f"Hi {appt.user.username},\n\nThis is a reminder for your appointment on {appt.date} at {appt.time}."
            recipient = [appt.user.email] if appt.user.email else []
            if recipient:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=True)

            # ---------------- SMS ----------------
            if hasattr(appt.user, 'phone_number') and appt.user.phone_number:
                send_sms(appt.user.phone_number, body)

            # Mark reminder as sent
            appt.reminder_sent = True
            appt.save()
