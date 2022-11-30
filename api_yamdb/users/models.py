from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    email = models.EmailField(
        _('email address'),
        max_length=254,   # новое
        unique=True)
    password = models.CharField(
        _('password'),
        max_length=128,
        blank=True)
    first_name = models.CharField(
        _('first name'),
        max_length=150,   # новое
        blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=20,
        blank=True,
    )
    objects = CustomUserManager()
