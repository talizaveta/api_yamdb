from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

USER = 'User'
MODERATOR = 'Moderator'
ADMIN = 'Admin'


class User(AbstractUser):
    """Модель для создания пользователя."""
    ROLE_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]
    username = models.CharField(
        'Имя профиля',
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        blank=False,
        null=False,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role[0]) for role in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        blank=True
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
