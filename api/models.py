from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Username is required!')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Period(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='periods'
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'start_date'])]

    def clean(self):
        if not self.start_date and not self.end_date:
            raise ValidationError('At least one date is required!')

    def __str__(self):
        return f'{self.user} - {self.start_date}'


class Metric(models.Model):
    slug = models.SlugField(unique=True)
    custom = models.BooleanField(default=False)
    multiple = models.BooleanField(default=False)

    def __str__(self):
        return str(self.slug)


class MetricOption(models.Model):
    label = models.CharField(max_length=100)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='options')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_options',
    )

    class Meta:
        indexes = [
            models.Index(fields=['metric']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return str(self.label)
