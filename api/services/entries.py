from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q

from api.models import Entry


@transaction.atomic
def create_entry(user, metric, option, entry_date=None):
    if not entry_date:
        entry_date = date.today()

    if entry_date > date.today():
        raise ValidationError('Entry cannot be in the future!')

    if metric.pk != option.metric.pk:
        raise ValidationError(f'{option.label} not allowed for {metric.slug}!')

    if (
        not metric.multiple
        and Entry.objects.filter(
            entry_date=entry_date, metric=metric, user=user
        ).exists()
    ):
        raise ValidationError(f'{metric.slug} already registered for this date!')

    if (
        metric.multiple
        and Entry.objects.filter(
            entry_date=entry_date, metric=metric, option=option, user=user
        ).exists()
    ):
        raise ValidationError(
            f'{metric.slug} already registered with {option.label} for this date!'
        )

    if option.user and option.user.pk != user.pk:
        raise ValidationError(
            'Custom options can only be used by the user who created them.'
        )

    period = user.periods.filter(
        Q(start_date__lte=entry_date)
        & (Q(end_date__gte=entry_date) | Q(end_date__isnull=True))
    ).first()

    if not period and metric.slug == 'flow':
        raise ValidationError('Metric not allowed for this date!.')

    return Entry.objects.create(
        user=user, period=period, metric=metric, option=option, entry_date=entry_date
    )
