from datetime import date

import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from .models import Metric, MetricOption, Period, User


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
def test_period_dates_validation():
    with pytest.raises(ValidationError):
        Period(user=create_user()).full_clean()


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
