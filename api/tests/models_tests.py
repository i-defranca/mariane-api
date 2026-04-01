from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from api.models import Entry

from .utils import new_metric, new_option, new_period, new_user, new_user_cycle


@mark.django_db
def test_username_validation():
    with pytest.raises(ValueError):
        new_user(None)


@mark.django_db
def test_user_creation():
    assert str(new_user('username')) == 'username'


@mark.django_db
def test_user_cycle_day_property():
    user = new_user()
    new_period(user, date.today() - timedelta(days=5), date.today() - timedelta(days=3))

    assert user.cycle_day == 6

    new_period(user)
    assert user.cycle_day == 1


@mark.django_db
def test_user_cycle_menstrual_phase_property():
    assert new_user_cycle(day=6).cycle_phase == 'menstrual'


@mark.django_db
def test_user_cycle_follicular_phase_property():
    assert new_user_cycle(day=18).cycle_phase == 'follicular'


@mark.django_db
def test_user_cycle_ovulation_window_phase_property():
    assert new_user_cycle(day=21).cycle_phase == 'ovulation window'


@mark.django_db
def test_user_cycle_luteal_phase_property():
    assert new_user_cycle(day=22).cycle_phase == 'luteal'


@mark.django_db
def test_entry_validation():
    user = new_user()
    metric = new_metric()
    option = new_option(metric)

    entry = Entry(
        user=user,
        metric=metric,
        option=option,
        entry_date=date(2026, 3, 2),
    )
    entry.save()

    assert str(entry) == f'{user} - {metric.slug} - {entry.entry_date}'

    entry = Entry(
        user=user,
        metric=metric,
        option=option,
        entry_date=date(2026, 3, 2),
    )
    with pytest.raises(ValidationError):
        entry.full_clean()


@mark.django_db
def test_metric_creation():
    assert str(new_metric('slug')) == 'slug'


@mark.django_db
def test_metric_option_creation():
    assert str(new_option(new_metric(), 'label')) == 'label'


@mark.django_db
def test_multiple_metric():
    user = new_user()

    metric = new_metric('food', True)
    option1 = new_option(metric, 'Apple')
    option2 = new_option(metric, 'Banana')

    entry1 = Entry(
        user=user,
        metric=metric,
        option=option1,
        entry_date=date(2026, 3, 2),
    )
    entry2 = Entry(
        user=user,
        metric=metric,
        option=option2,
        entry_date=date(2026, 3, 2),
    )
    entry1.full_clean()
    entry2.full_clean()
    entry1.save()
    entry2.save()

    assert Entry.objects.filter(metric=metric).count() == 2
