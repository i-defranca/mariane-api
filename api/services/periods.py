from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from api.models import Entry, Period


def link_entries(p):
    Entry.objects.filter(
        entry_date__gte=p.start_date or date.min,
        entry_date__lte=p.end_date or date.max,
        user=p.user,
    ).update(period=p)

    return p


@transaction.atomic
def create_period(user, start_date=None, end_date=None):
    if not start_date:
        start_date = date.today()

    if start_date and end_date and end_date <= start_date:
        raise ValidationError('Start date must be before end!')

    if not end_date and user.periods.filter(end_date__isnull=True).exists():
        raise ValidationError('You already have an open period!')

    overlap = user.periods.filter(
        start_date__lte=end_date or date.max,
        end_date__gte=start_date,
    )
    future = user.periods.filter(start_date__gte=start_date)

    if not end_date and future.exists() or overlap.exists():
        raise ValidationError('Periods cannot overlap!')

    period = Period.objects.create(user=user, start_date=start_date, end_date=end_date)
    return link_entries(period)


@transaction.atomic
def update_period(period, **changes):
    obj = period

    for k, v in changes.items():
        setattr(obj, k, v)

    if not obj.start_date:
        raise ValidationError('Start date is required!')

    if obj.end_date and obj.end_date <= obj.start_date:
        raise ValidationError('Start date must be before end!')

    overlap = obj.user.periods.filter(
        start_date__lte=obj.end_date or date.max,
        end_date__gte=obj.start_date,
    ).exclude(pk=obj.pk)
    future = obj.user.periods.filter(start_date__gte=obj.start_date)

    if not obj.end_date and future.exists() or overlap.exists():
        raise ValidationError('Periods cannot overlap!')

    obj.save()

    return link_entries(obj)
