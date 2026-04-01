from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from api.models import Entry, MetricOption, Period

from .utils import (
    new_empty_period,
    new_entry,
    new_metric,
    new_option,
    new_period,
    new_user,
)


@mark.django_db
def test_period_creation():
    user = new_user()
    period = new_period(user)

    assert Period.objects.count() == 1
    assert str(period) == f'{user} - {period.start_date}'


@mark.django_db
def test_option_creation():
    option = new_option(new_metric(), 'label')
    assert MetricOption.objects.count() == 1
    assert str(option) == 'label'


@mark.django_db
def test_entry_creation():
    user = new_user()
    period = new_period(user)
    metric = new_metric()

    entry = new_entry(user, metric)

    assert Entry.objects.count() == 1
    assert entry.period.pk == period.pk
    assert str(entry) == f'{user} - {metric.slug} - {entry.entry_date}'


# Period | validations
@mark.django_db
def test_period_dates_filled_validation():
    with pytest.raises(ValidationError):
        new_empty_period()


@mark.django_db
def test_period_dates_ordering_validation():
    with pytest.raises(ValidationError):
        new_period(end=date.today() - timedelta(days=5))


@mark.django_db
def test_period_user_has_open_validation():
    user = new_user()
    new_empty_period(user, start=date.today(), end=None)
    with pytest.raises(ValidationError):
        new_period(user)


@mark.django_db
def test_period_overlap_validation():
    user = new_user()

    new_period(user, start=date(2026, 1, 1), end=date(2026, 1, 20))
    with pytest.raises(ValidationError):
        new_period(user, start=date(2026, 1, 15))


# Entry | validations
@mark.django_db
def test_entry_future_date_validation():
    with pytest.raises(ValidationError):
        new_entry(entry_date=date.today() + timedelta(days=5))


@mark.django_db
def test_entry_option_metric_validation():
    with pytest.raises(ValidationError):
        new_entry(option=new_option(new_metric()))


@mark.django_db
def test_entry_duplicate_metric_validation():
    user = new_user()
    metric = new_metric()
    new_entry(user, metric)
    with pytest.raises(ValidationError):
        new_entry(user, metric)


@mark.django_db
def test_entry_duplicate_option_validation():
    user = new_user()
    metric = new_metric(multiple=True)
    option = new_option(metric)
    new_entry(user, metric, option)
    with pytest.raises(ValidationError):
        new_entry(user, metric, option)


@mark.django_db
def test_entry_custom_option_ownership_validation():
    user = new_user()
    metric = new_metric()
    option = new_option(metric, user=new_user())
    with pytest.raises(ValidationError):
        new_entry(user, metric, option)


@mark.django_db
def test_entry_flow_metric_no_period_validation():
    user = new_user()
    metric = new_metric('flow')
    with pytest.raises(ValidationError):
        new_entry(user, metric)


@mark.django_db
def test_entry_allow_multiple_metric():
    user = new_user()

    metric = new_metric('food', True)

    new_entry(user, metric, new_option(metric, 'Apple'))
    new_entry(user, metric, new_option(metric, 'Banana'))

    assert Entry.objects.filter(metric=metric).count() == 2


# Option | validations
@mark.django_db
def test_option_empty_metric_validation():
    with pytest.raises(ValidationError):
        new_option()


@mark.django_db
def test_option_empty_label_validation():
    with pytest.raises(ValidationError):
        new_option(new_metric(), empty=True)


@mark.django_db
def test_option_not_custom_metric_validation():
    with pytest.raises(ValidationError):
        new_option(new_metric(custom=False))


@mark.django_db
def test_option_duplicate_user_label_metric_validation():
    user = new_user()
    metric = new_metric()
    new_option(metric, 'label', user)
    with pytest.raises(ValidationError):
        new_option(metric, 'label', user)


@mark.django_db
def test_option_duplicate_label_metric_validation():
    metric = new_metric()
    new_option(metric, 'label')
    with pytest.raises(ValidationError):
        new_option(metric, 'label', new_user())
