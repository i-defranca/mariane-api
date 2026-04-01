
from django.core.exceptions import ValidationError
from django.db import transaction

from api.models import MetricOption


@transaction.atomic
def create_option(user, metric, label):
    if not metric:
        raise ValidationError('It must belong to a metric!')

    if not metric.custom:
        raise ValidationError(f'{metric.slug} does not allow custom options!')

    if not label:
        raise ValidationError('It should have a label!')

    if user and user.custom_options.filter(metric=metric, label=label).exists():
        raise ValidationError(
            f'You already defined an option with this label for {metric.slug}!'
        )

    if MetricOption.objects.filter(
        user__isnull=True, metric=metric, label=label
    ).exists():
        raise ValidationError(
            f"There's already an option with this label for {metric.slug}!"
        )

    return MetricOption.objects.create(user=user, metric=metric, label=label)
