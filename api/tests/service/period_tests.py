from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from api.models import Period
from api.tests import (
    new_empty_period,
    new_entry,
    new_metric,
    new_period,
    new_user,
    upd_period,
)


@mark.django_db
def test_creation():
    user = new_user()
    period = new_period(user)

    assert Period.objects.count() == 1
    assert str(period) == f'{user} - {period.start_date}'


# update
@mark.django_db
def test_start_date_update():
    user = new_user()
    period = new_period(user)

    start = date.today() - timedelta(days=1)
    upd_period(period, start=start)

    assert Period.objects.count() == 1
    period.refresh_from_db()
    assert period.start_date == start


@mark.django_db
def test_end_date_update():
    user = new_user()
    period = new_period(user)

    end = date.today() + timedelta(days=2)
    upd_period(period, end=end)

    assert Period.objects.count() == 1
    period.refresh_from_db()
    assert period.end_date == end


# validations
@mark.django_db
def test_dates_filled_validation():
    with pytest.raises(ValidationError):
        new_empty_period()


@mark.django_db
def test_creation_dates_ordering_validation():
    with pytest.raises(ValidationError):
        new_period(end=date.today() - timedelta(days=5))


@mark.django_db
def test_update_dates_ordering_validation():
    period = new_period()
    with pytest.raises(ValidationError):
        upd_period(period, end=date.today() - timedelta(days=5))


@mark.django_db
def test_user_has_open_validation():
    user = new_user()
    new_empty_period(user, start=date.today(), end=None)
    with pytest.raises(ValidationError):
        new_period(user)


@mark.django_db
def test_creation_overlap_validation():
    user = new_user()

    new_period(user, start=date(2026, 1, 1), end=date(2026, 1, 20))
    with pytest.raises(ValidationError):
        new_period(user, start=date(2026, 1, 15))


@mark.django_db
def test_update_overlap_validation():
    user = new_user()

    new_period(user, start=date(2026, 1, 1), end=date(2026, 1, 20))
    period = new_period(user)
    with pytest.raises(ValidationError):
        upd_period(period, start=date(2026, 1, 15), end=date(2026, 1, 19))


# entries linking
@mark.django_db
def test_creation_entries_linking():
    user = new_user()
    entry = new_entry(user, new_metric())
    other_user_entry = new_entry(new_user(), new_metric())

    assert entry.period is None
    assert other_user_entry.period is None

    period = new_period(user)
    new_period(new_user())

    entry.refresh_from_db()
    other_user_entry.refresh_from_db()

    assert entry.period.pk == period.pk
    assert other_user_entry.period is None


@mark.django_db
def test_update_entries_linking():
    user = new_user()
    dt = date.today() - timedelta(days=20)
    entry = new_entry(user, new_metric(), entry_date=dt)
    other_user_entry = new_entry(new_user(), new_metric(), entry_date=dt)

    assert entry.period is None
    assert other_user_entry.period is None

    period = new_period(user)
    other_user_period = new_period(new_user())

    entry.refresh_from_db()
    other_user_entry.refresh_from_db()

    assert entry.period is None
    assert other_user_entry.period is None

    dtt = dt - timedelta(days=1)
    upd_period(period, start=dtt)
    upd_period(other_user_period, start=dtt)

    entry.refresh_from_db()
    other_user_entry.refresh_from_db()

    assert entry.period.pk == period.pk
    assert other_user_entry.period is None
