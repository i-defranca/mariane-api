from datetime import date, timedelta

from api.models import Metric, MetricOption, User
from api.services import create_period


def new_user(username='username'):
    return User.objects.create_user(username=username)


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


def new_metric(slug='mood', multiple=False):
    return Metric.objects.create(slug=slug, multiple=multiple)


def new_option(metric, label='Happy'):
    return MetricOption.objects.create(label=label, metric=metric)


def new_user_cycle(day):
    user = new_user()

    new_period(user, date(2026, 1, 1), date(2026, 1, 31))  # avg 30

    new_empty_period(user, date.today() - timedelta(days=day - 1), None)

    return user
