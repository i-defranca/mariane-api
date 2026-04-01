from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from api.models import Period


@transaction.atomic
def create_period(user, start_date=None, end_date=None):
    if not start_date and not end_date:
        raise ValidationError('At least one date is required!')

    if start_date and end_date and end_date <= start_date:
        raise ValidationError('Start date must be before end!')

    if user.periods.filter(end_date__isnull=True).exists():
        raise ValidationError('You already have an open period!')

    if user.periods.filter(
        start_date__lte=end_date or date.max, end_date__gte=start_date or date.min
    ).exists():
        raise ValidationError('Periods cannot overlap!')

    return Period.objects.create(user=user, start_date=start_date, end_date=end_date)
