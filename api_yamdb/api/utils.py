import secrets
import string

from django.core.mail import send_mail


def generate_alphanum_crypt_string(length):
    '''
    Генерирует строку из цифр, заглавных и строчных букв заданной длины
    '''
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(length))
    return crypt_rand_string


def EmailConfirmationCode(confirmation_code, username, email):
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
