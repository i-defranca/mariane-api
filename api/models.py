from datetime import date
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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

    @property
    def cycle_day(self):
        today = date.today()

        last = (
            self.periods.filter(start_date__lte=today)
            .order_by('-start_date')
            .values_list('start_date', flat=True)
            .first()
            or today
        )

        return (today - last).days + 1

    @property
    def cycle_phase(self):
        avg = round(
            self.periods.filter(start_date__isnull=False, end_date__isnull=False)
            .aggregate(
                avg_days=models.Avg(models.F('end_date') - models.F('start_date'))
            )['avg_days']
            .total_seconds()
            / 86400,
            2,
        )
        if self.cycle_day <= int(avg * 0.2):
            return 'menstrual'
        elif self.cycle_day <= int(avg * 0.6):
            return 'follicular'
        elif self.cycle_day <= int(avg * 0.7):
            return 'ovulation window'
        else:
            return 'luteal'

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


class Entry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entries'
    )
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='entries', null=True, blank=True
    )
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='entries')
    option = models.ForeignKey(
        MetricOption, on_delete=models.CASCADE, related_name='entries'
    )
    entry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'entry_date']),
        ]

    def __str__(self):
        return f'{self.user} - {self.metric.slug} - {self.entry_date}'
