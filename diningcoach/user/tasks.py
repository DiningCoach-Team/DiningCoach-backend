from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from celery import shared_task


@shared_task
def add(x, y):
  return x + y


@shared_task(bind=False)
def signup_complete_send_email(username, email):
  subject = '[DiningCoach Team] Thank you for joining DiningCoach'
  message = f'Hello {username},\n\nYou have successfully signed up for DiningCoach.\nFeel free to enjoy!\n\nRegards,\nDiningCoach Team'
  from_email = settings.EMAIL_HOST_USER

  # email_message = EmailMessage(
  #   subject=subject,
  #   body=message,
  #   from_email=from_email,
  #   to=[email]
  # )
  # email_message.send()

  email_message = {
    'subject': subject,
    'message': message,
    'from_email': from_email,
    'recipient_list': [email],
  }
  send_mail(**email_message)


@shared_task(bind=False)
def password_reset_send_email(msg):
  msg.send()
