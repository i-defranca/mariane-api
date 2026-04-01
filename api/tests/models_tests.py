from datetime import date, timedelta

import pytest
from pytest import mark

from .utils import new_metric, new_option, new_period, new_user, new_user_cycle


@mark.django_db
def test_user_creation():
    assert str(new_user('username')) == 'username'


@mark.django_db
def test_metric_creation():
    assert str(new_metric('slug')) == 'slug'


@mark.django_db
def test_metric_option_creation():
    assert str(new_option(new_metric(), 'label')) == 'label'


# User | validation
@mark.django_db
def test_username_validation():
    with pytest.raises(ValueError):
        new_user(None, True)


# User | properties
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

