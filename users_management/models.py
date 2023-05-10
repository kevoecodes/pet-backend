from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from users_management.user_manager import UserManager


class User(AbstractUser):
    ADMIN = 0
    USER = 1

    ROLES = (
        (ADMIN, 'Admin'),
        (USER, 'USER')
    )

    first_name = models.CharField(verbose_name='First Name', max_length=100)
    last_name = models.CharField(verbose_name='Last Name', max_length=100)
    role = models.IntegerField(choices=ROLES, default=ADMIN)

    national_id = models.IntegerField(verbose_name='National ID Number', null=True)
    cellphone = models.CharField(max_length=50, unique=True, verbose_name='Phone Number')
    email = models.EmailField(verbose_name='Email', unique=True, max_length=100, blank=False)
    username = models.CharField(verbose_name='User Name', max_length=50, blank=True, null=True)

    password_changed = models.BooleanField(default=False)

    email_confirmed = models.BooleanField(default=False)
    cellphone_confirmed = models.BooleanField(default=False)

    profile_photo = models.CharField(max_length=255, null=True, blank=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cellphone']

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.get_full_name()
