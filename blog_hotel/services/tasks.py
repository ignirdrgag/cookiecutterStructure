from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Reservation

@shared_task
def send_reservation_confirmation(reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        subject = 'Confirmation de votre réservation'
        html_message = render_to_string('services/emails/reservation_confirmation.html', {
            'user': reservation.user,
            'reservation': reservation,
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [reservation.user.email]

        send_mail(
            subject=subject,
            message="Votre réservation a été confirmée.",  # Fallback texte brut
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
    except Reservation.DoesNotExist:
        # Log l'erreur si nécessaire (optionnel)
        pass