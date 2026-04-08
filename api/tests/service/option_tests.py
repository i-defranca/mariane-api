import pytest
from django.core.exceptions import ValidationError

from api.models import MetricOption


def test_option_creation(user, option):
    option.create()
    option.create()

    assert MetricOption.objects.count() == 2

    other = user.create()
    option.create(user=other)
    option.create(user=other)

    option.create(user=None)
    option.create(user=None)

    assert MetricOption.objects.count() == 6
    assert MetricOption.objects.filter(user=other).count() == 2
    assert MetricOption.objects.filter(user=user.obj).count() == 2
    assert MetricOption.objects.filter(user__isnull=True).count() == 2


def test_option_empty_metric_validation(option):
    # TODO: {error:{metric:'empty'}}
    with pytest.raises(ValidationError):
        option.create(metric=None)


def test_option_empty_label_validation(option):
    # TODO: {error:{label:'empty'}}
    with pytest.raises(ValidationError):
        option.create(label='')


def test_option_not_custom_metric_validation(metric, option):
    # TODO: {error:{metric:'not_custom'}}
    with pytest.raises(ValidationError):
        option.create(metric=metric(custom=False))


def test_option_duplicate_user_label_metric_validation(option):
    # TODO: {error:{label:'exists_user'}}
    with pytest.raises(ValidationError):
        option.create(label=option.obj.label)


def test_option_duplicate_label_metric_validation(user, option):
    option.create(user=None)
    # TODO: {error:{label:'exists_global'}}
    with pytest.raises(ValidationError):
        option.create(label=option.obj.label, user=user.create())
