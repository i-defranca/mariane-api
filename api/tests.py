from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from .models import Entry, Metric, MetricOption, Period, User


def test_api_health(client):
    response = client.get('/api/')
    assert response.status_code == 200


def create_user(username='username'):
    return User.objects.create_user(username=username)


def create_metric(slug='mood', multiple=False):
    return Metric.objects.create(slug=slug, multiple=multiple)


def create_option(metric, label='Happy'):
    return MetricOption.objects.create(label=label, metric=metric)


@mark.django_db
def test_username_validation():
    with pytest.raises(ValueError):
        create_user(None)


@mark.django_db
def test_user_creation():
    assert str(create_user('username')) == 'username'


@mark.django_db
def test_user_cycle_day_property():
    user = create_user()
    Period.objects.create(user=user, start_date=date.today() - timedelta(days=5))

    assert user.cycle_day == 6

    Period.objects.create(user=user, start_date=date.today())
    assert user.cycle_day == 1


def create_user_cycle(day):
    user = create_user()

    Period.objects.create(
        user=user, start_date=date(2026, 1, 1), end_date=date(2026, 1, 31)
    )  # avg 30
    Period.objects.create(user=user, start_date=date.today() - timedelta(days=day - 1))

    return user


@mark.django_db
def test_user_cycle_menstrual_phase_property():
    assert create_user_cycle(day=6).cycle_phase == 'menstrual'


@mark.django_db
def test_user_cycle_follicular_phase_property():
    assert create_user_cycle(day=18).cycle_phase == 'follicular'


@mark.django_db
def test_user_cycle_ovulation_window_phase_property():
    assert create_user_cycle(day=21).cycle_phase == 'ovulation window'


@mark.django_db
def test_user_cycle_luteal_phase_property():
    assert create_user_cycle(day=22).cycle_phase == 'luteal'


@mark.django_db
def test_period_dates_validation():
    with pytest.raises(ValidationError):
        Period(user=create_user()).full_clean()


@mark.django_db
def test_entry_validation():
    user = create_user()
    metric = create_metric()
    option = create_option(metric)

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
def test_period_creation():
    user = create_user()

    period = Period(user=user, start_date=date(2026, 3, 1), end_date=date(2026, 3, 5))
    period.full_clean()
    period.save()

    assert Period.objects.count() == 1
    assert str(period) == f'{user} - {period.start_date}'


@mark.django_db
def test_metric_creation():
    assert str(create_metric('slug')) == 'slug'


@mark.django_db
def test_metric_option_creation():
    assert str(create_option(create_metric(), 'label')) == 'label'


@mark.django_db
def test_multiple_metric():
    user = create_user()

    metric = create_metric('food', True)
    option1 = create_option(metric, 'Apple')
    option2 = create_option(metric, 'Banana')

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
