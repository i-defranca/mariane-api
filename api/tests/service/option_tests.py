import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from api.models import MetricOption
from api.tests import new_metric, new_option, new_user


@mark.django_db
def test_option_creation():
    option = new_option(new_metric(), 'label')
    assert MetricOption.objects.count() == 1
    assert str(option) == 'label'


# validations
@mark.django_db
def test_option_empty_metric_validation():
    with pytest.raises(ValidationError):
        new_option()


@mark.django_db
def test_option_empty_label_validation():
    with pytest.raises(ValidationError):
        new_option(new_metric(), '')


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
