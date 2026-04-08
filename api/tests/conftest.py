from datetime import date, timedelta
from random import choice
from string import ascii_lowercase as asc

import pytest

from api.models import Metric, User
from api.services import create_entry, create_option, create_period, update_period


def parse(**kwargs):
    for k, v in kwargs.items():
        if isinstance(v, str) and k.endswith('_date'):
            kwargs[k] = date.fromisoformat(v)
    return kwargs


class ModelFactory:
    def __init__(self, create, update=None):
        self._create = create
        self._update = update
        self._instance = None

    def __call__(self, **kwargs):
        return self._obj(self._create(**parse(**kwargs)))

    def create(self, **kwargs):
        return self._obj(self._create(**parse(**kwargs)))

    def update(self, **kwargs):
        kwargs.setdefault('period', self.obj)
        return self._obj(self._update(**parse(**kwargs)) if self._update else None)

    def _obj(self, val=None):
        if self._instance is None:
            self._instance = val if val is not None else self._create()
        return val

    @property
    def obj(self):
        return self._obj() or self._instance


@pytest.fixture
def user(db, lorem):
    def _create(**kwargs):
        kwargs.setdefault('username', lorem(8))
        kwargs.setdefault('password', lorem(16))
        user = User.objects.create_user(**kwargs)
        user.raw_password = kwargs.get('password')
        return user

    return ModelFactory(_create)


@pytest.fixture
def metric(db, lorem):
    def _create(**kwargs):
        kwargs.setdefault('slug', lorem())
        kwargs.setdefault('custom', True)
        kwargs.setdefault('multiple', False)
        return Metric.objects.create(**kwargs)

    return ModelFactory(_create)


@pytest.fixture
def option(db, user, metric, lorem):
    def _create(**kwargs):
        kwargs.setdefault('user', user.obj)
        kwargs.setdefault('label', lorem())
        kwargs.setdefault('metric', metric.obj)
        return create_option(**kwargs)

    return ModelFactory(_create)


@pytest.fixture
def period(db, user, today):
    def _create(**kwargs):
        kwargs.setdefault('user', user.obj)
        kwargs.setdefault('start_date', today())
        kwargs.setdefault('end_date', today(1))
        return create_period(**kwargs)

    def _update(**kwargs):
        return update_period(**kwargs)

    return ModelFactory(_create, _update)


@pytest.fixture
def entry(db, user, metric, option):
    def _create(**kwargs):
        kwargs.setdefault('user', user.obj)
        kwargs.setdefault('metric', metric.create())
        opt = option(metric=kwargs.get('metric'), user=kwargs.get('user'))
        kwargs.setdefault('option', opt)
        return create_entry(**kwargs)

    return ModelFactory(_create)


@pytest.fixture
def lorem():
    def _lorem(len=4):
        return ''.join(choice(asc) for _ in range(len))

    return _lorem


@pytest.fixture
def today():
    def _today(days=0):
        dt = date.today()
        if days != 0:
            delta = timedelta(days=abs(days))
            return dt + delta if days > 0 else dt - delta
        return dt

    return _today
