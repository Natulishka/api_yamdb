from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUserManager(BaseUserManager):
    '''
    При создании суперпользователя проставляет пользовательскую роль admin и
    не позволяет создать пользователя с username me
    '''
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('Username must be set'))
        if username == 'me':
            raise ValueError(_("Username can't be 'me'"))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          username=username,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True)
    password = models.CharField(
        _('password'),
        max_length=128,
        blank=True)
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default='user',
    )
    # confirmation_code = models.TextField(
    #     'Код подтверждения',
    #     blank=True,
    # )
    objects = CustomUserManager()
