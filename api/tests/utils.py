from datetime import date, timedelta
from random import choice
from string import ascii_lowercase as asc

from api.models import Metric, User
from api.services import create_entry, create_option, create_period, update_period


def lorem(len=4):
    return ''.join(choice(asc) for _ in range(len))


def new_user(username=None, empty=False):
    if not username and not empty:
        username = lorem(8)
    return User.objects.create_user(username=username)


def new_entry(user=None, metric=None, option=None, entry_date=None):
    if not user:
        user = new_user()
    if not metric:
        metric = new_metric()
    if not option:
        option = new_option(metric)

    return create_entry(
        user=user,  # type: ignore
        metric=metric,  # type: ignore
        option=option,  # type: ignore
        entry_date=entry_date,  # type: ignore
    )


def new_period(user=None, start=None, end=None):
    if not user:
        user = new_user()
    if not start:
        start = date.today()
    if not end:
        end = date.today() + timedelta(days=1)

    return create_period(
        user=user,  # type: ignore
        start_date=start,  # type: ignore
        end_date=end,  # type: ignore
    )


def new_empty_period(user=None, start=None, end=None):
    if not user:
        user = new_user()

    return create_period(
        user=user,  # type: ignore
        start_date=start,  # type: ignore
        end_date=end,  # type: ignore
    )


def upd_period(period, start=None, end=None):
    changes = {}
    if start:
        changes['start_date'] = start
    if end:
        changes['end_date'] = end
    return update_period(period, **changes)  # type: ignore


def new_metric(slug=None, multiple=False, custom=True):
    if not slug:
        slug = lorem()
    return Metric.objects.create(slug=slug, custom=custom, multiple=multiple)


def new_option(metric=None, label=None, user=None, empty=False):
    if not label and not empty:
        label = lorem()
    return create_option(user=user, metric=metric, label=label)  # type: ignore


def new_user_cycle(day):
    user = new_user()

    new_period(user, date(2026, 1, 1), date(2026, 1, 31))  # avg 30

    new_empty_period(user, date.today() - timedelta(days=day - 1), None)

    return user
