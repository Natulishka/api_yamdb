from django.core.mail import send_mail


def email_confirmation_code(confirmation_code, username, email):
    '''
    Отправляет письмо с кодом подтверждения
    '''
    body = f'Hello, {username}, your confirmation code is {confirmation_code}.'
    send_mail(
        'Confirmation code',
        body,
        'from@example.com',
        [email],
        fail_silently=False,)
