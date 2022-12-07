from django.conf import settings
from django.core.mail import send_mail


def send_email_confirmation_code(confirmation_code, username, email):
    '''
    Отправляет письмо с кодом подтверждения
    '''
    body = f'Hello, {username}, your confirmation code is {confirmation_code}.'
    send_mail(
        'Confirmation code',
        body,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,)
