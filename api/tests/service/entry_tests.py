import pytest
from django.core.exceptions import ValidationError

from api.models import Entry


def test_outside_period_creation(entry, today):
    entry.create()
    other = entry.create(entry_date=today(-3))

    assert other.period is None
    assert entry.obj.period is None
    assert Entry.objects.count() == 2


def test_inside_period_creation(entry, period):
    period.create()
    entry.create()

    assert entry.obj.period.pk == period.obj.pk


def test_multiple_metric_creation(entry, metric):
    metric.create(multiple=True)

    entry.create()
    entry.create(metric=metric.obj)
    entry.create(metric=metric.obj)

    assert Entry.objects.filter(metric=metric.obj).count() == 2


def test_future_date_validation(entry, today):
    # TODO: {error:{entry_date:'future'}}
    with pytest.raises(ValidationError):
        entry.create(entry_date=today(5))


def test_option_metric_validation(entry, metric, option):
    # TODO: {error:{option:'not_allowed_for_metric'}}
    with pytest.raises(ValidationError):
        entry.create(option=option.create(metric=metric.obj))


def test_duplicate_metric_validation(entry, metric):
    entry.create(metric=metric.create(multiple=False))
    # TODO: {error:{metric:'not_multiple'}}
    with pytest.raises(ValidationError):
        entry.create(metric=metric.obj)


def test_duplicate_option_validation(entry, metric, option):
    entry.create(metric=metric.create(multiple=True))
    # TODO: {error:{metric:'option_exists'}}
    with pytest.raises(ValidationError):
        entry.create(metric=metric.obj, option=option.obj)


def test_custom_option_ownership_validation(user, entry, metric, option):
    option.create()
    # TODO: {error:{option:'not_owner'}}
    with pytest.raises(ValidationError):
        entry.create(user=user.create(), metric=metric.obj, option=option.obj)


def test_flow_metric_no_period_validation(entry, metric):
    # TODO: {error:{metric:'not_allowed_outside_period'}}
    with pytest.raises(ValidationError):
        entry.create(metric=metric.create(slug='flow'))
