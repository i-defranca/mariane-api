from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from api.models import Period

from .utils import new_empty_period, new_period, new_user


@mark.django_db
def test_period_creation():
    user = new_user()
    period = new_period(user=user)

    assert Period.objects.count() == 1
    assert str(period) == f'{user} - {period.start_date}'


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
