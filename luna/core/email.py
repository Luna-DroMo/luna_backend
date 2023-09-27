from django.core.mail import send_mail
import random
from django.conf import settings

# from .models import User


def send_otp_via_email(email):
    subject = "Account verification email"
    otp = random.randint(1000, 9999)
    message = f"Your One Time Password for account verification is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    # user_obj = User.objects.get(email = email)
    return otp
