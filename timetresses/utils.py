from email.utils import formataddr

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Erősítse meg a fiókját'
    message = render_to_string('account/email/account_verification_email.html', {
        'user': user,
        'current_site': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)

    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email],from_email="MyTimes.hu <mytimesdev@gmail.com")

    mail.send()


def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Jelszó visszaállítás'
    message = render_to_string('account/email/reset_password_email.html', {
        'user': user,
        'current_site': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)

    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email],from_email="MyTimes.hu <mytimesdev@gmail.com")

    mail.send()


def send_accept_mail(request, booking):
    current_site = get_current_site(request)
    mail_subject = 'Foglalása megerősítve'
    message = render_to_string('booking/email/accept_booking_mail.html', {
        'booking': booking,
        'current_site': current_site,
    })
    to_email = booking.booked_user.user.email
    mail = EmailMessage(mail_subject, message, to=[to_email],from_email="MyTimes.hu <mytimesdev@gmail.com")

    mail.send()


def send_not_accept_mail(request, booking):
    current_site = get_current_site(request)
    mail_subject = 'Foglalása törlése'
    message = render_to_string('booking/email/not_accept_booking_mail.html', {
        'booking': booking,
        'current_site': current_site,
    })
    to_email = booking.booked_user.user.email
    mail = EmailMessage(mail_subject, message, to=[to_email],from_email="MyTimes.hu <mytimesdev@gmail.com")
    mail.send()

def send_new_booking_mail(request,booking):
    current_site = get_current_site(request)
    mail_subject = 'Új foglalás'
    message = render_to_string('booking/email/new_booking.html', {
        'booking': booking,
        'current_site': current_site,
    })
    to_email = booking.service.user_profile.get_email()
    mail = EmailMessage(mail_subject, message, to=[to_email], from_email="MyTimes.hu <mytimesdev@gmail.com")
    mail.send()