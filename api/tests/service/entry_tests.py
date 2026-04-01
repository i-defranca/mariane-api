from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from api.models import Entry
from api.tests import new_entry, new_metric, new_option, new_period, new_user


@mark.django_db
def test_creation():
    user = new_user()
    period = new_period(user)
    metric = new_metric()

    entry = new_entry(user, metric)

    assert Entry.objects.count() == 1
    assert entry.period.pk == period.pk
    assert str(entry) == f'{user} - {metric.slug} - {entry.entry_date}'


# validations
@mark.django_db
def test_future_date_validation():
    with pytest.raises(ValidationError):
        new_entry(entry_date=date.today() + timedelta(days=5))


@mark.django_db
def test_option_metric_validation():
    with pytest.raises(ValidationError):
        new_entry(option=new_option(new_metric()))


@mark.django_db
def test_duplicate_metric_validation():
    user = new_user()
    metric = new_metric()
    new_entry(user, metric)
    with pytest.raises(ValidationError):
        new_entry(user, metric)


@mark.django_db
def test_duplicate_option_validation():
    user = new_user()
    metric = new_metric(multiple=True)
    option = new_option(metric)
    new_entry(user, metric, option)
    with pytest.raises(ValidationError):
        new_entry(user, metric, option)


@mark.django_db
def test_custom_option_ownership_validation():
    user = new_user()
    metric = new_metric()
    option = new_option(metric, user=new_user())
    with pytest.raises(ValidationError):
        new_entry(user, metric, option)


@mark.django_db
def test_flow_metric_no_period_validation():
    user = new_user()
    metric = new_metric('flow')
    with pytest.raises(ValidationError):
        new_entry(user, metric)


@mark.django_db
def test_allow_multiple_metric():
    user = new_user()

    metric = new_metric('food', True)

    new_entry(user, metric, new_option(metric, 'Apple'))
    new_entry(user, metric, new_option(metric, 'Banana'))

    assert Entry.objects.filter(metric=metric).count() == 2
