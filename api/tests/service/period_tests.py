import pytest
from django.core.exceptions import ValidationError

from api.models import Period


def test_creation(user, period, today):
    empty = period.create(user=user.obj, start_date=None, end_date=None)
    period.create(user=user.obj, start_date=today(-9), end_date=today(-5))

    period.create(user=(other := user.create()))

    assert empty.start_date == today()

    assert Period.objects.count() == 3
    assert Period.objects.filter(user=other).count() == 1
    assert Period.objects.filter(user=user.obj).count() == 2


def test_update(period, user, today):
    period.create()
    period.create(user=user.obj, start_date=today(-5), end_date=today(-3))

    period.update(start_date=today(-1))
    period.obj.refresh_from_db()
    assert period.obj.start_date == today(-1)

    period.update(end_date=today(2))
    period.obj.refresh_from_db()
    assert period.obj.end_date == today(2)

    period.update(start_date=today(-2), end_date=today(1))
    period.obj.refresh_from_db()
    assert period.obj.end_date == today(1)
    assert period.obj.start_date == today(-2)


def test_update_start_date_required(period):
    # TODO: {error:'dates_required'}
    with pytest.raises(ValidationError):
        period.update(start_date=None)


def test_creation_dates_ordering_validation(period, today):
    # TODO: {error:'dates_ordering'}
    with pytest.raises(ValidationError):
        period.create(end_date=today(-5))


def test_update_dates_ordering_validation(period, today):
    # TODO: {error:'dates_ordering'}
    with pytest.raises(ValidationError):
        period.update(end_date=today(-5))


def test_user_has_open_validation(period, today):
    period.create(start_date=today(-10), end_date=None)
    # TODO: {error:'open_period_exists'}
    with pytest.raises(ValidationError):
        period.create(end_date=None)


def test_creation_overlap_validation(period):
    period.create(start_date='2026-01-01', end_date='2026-01-20')
    # TODO: {error:'periods_overlap'}
    with pytest.raises(ValidationError):
        period.create(start_date='2026-01-15', end_date='2026-01-19')


def test_creation_future_overlap_validation(period):
    period.create(start_date='2026-05-01', end_date='2026-05-20')
    # TODO: {error:'periods_overlap'}
    with pytest.raises(ValidationError):
        period.create(start_date='2026-04-01', end_date=None)


def test_update_overlap_validation(period):
    period.create()
    period.create(start_date='2026-01-01', end_date='2026-01-20')
    # TODO: {error:'periods_overlap'}
    with pytest.raises(ValidationError):
        period.update(start_date='2026-01-15', end_date='2026-01-19')


def test_update_future_overlap_validation(period):
    period.create()
    period.create(start_date='2026-05-01', end_date='2026-05-20')
    # TODO: {error:'periods_overlap'}
    with pytest.raises(ValidationError):
        period.update(start_date='2026-04-01', end_date=None)


# entries linking
def test_creation_entries_linking(user, entry, period):
    entry.create()
    other = entry.create(user=user.create())

    assert other.period is None
    assert entry.obj.period is None

    period.create()
    period.create(user=user.create())

    other.refresh_from_db()
    entry.obj.refresh_from_db()

    assert other.period is None
    assert entry.obj.period.pk == period.obj.pk


def test_update_entries_linking(user, entry, period, today):
    entry.create(entry_date=today(-20))
    other = entry.create(user=user.create(), entry_date=today(-20))

    period.create()
    other_period = period.create(user=user.create())

    other.refresh_from_db()
    entry.obj.refresh_from_db()

    assert other.period is None
    assert entry.obj.period is None

    period.update(period=period.obj, start_date=today(-20 - 1))
    period.update(period=other_period, start_date=today(-20 - 1))

    other.refresh_from_db()
    entry.obj.refresh_from_db()

    assert other.period is None
    assert entry.obj.period.pk == period.obj.pk
