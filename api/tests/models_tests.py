import pytest


@pytest.fixture
def fmt():
    def resolve(obj, path):
        for attr in path.split('.'):
            obj = getattr(obj, attr)
        return obj

    def _format(fields, obj):
        template = ' - '.join(str(resolve(obj, _)) for _ in fields)
        return str(obj) == template.format(**obj.__dict__)

    return _format


def test_user_string_representation(user, fmt):
    assert fmt(['username'], user.obj)
    assert fmt(['username'], user.obj)


def test_period_string_representation(period, fmt):
    assert fmt(['user', 'start_date'], period.obj)


def test_metric_string_representation(metric, fmt):
    assert fmt(['slug'], metric.obj)


def test_option_string_representation(option, fmt):
    assert fmt(['label'], option.obj)


def test_entry_string_representation(entry, fmt):
    assert fmt(['user', 'metric', 'entry_date'], entry.obj)


def test_username_validation(user):
    with pytest.raises(ValueError):
        user.create(username='')


def test_user_cycle_day_property(user, today, period):
    assert user.obj.cycle_day == 0

    period.create(start_date=today(-5), end_date=today(-3))

    assert user.obj.cycle_day == 6

    period.create(user=user.obj)
    assert user.obj.cycle_day == 1


@pytest.fixture
def cycle_phase(user, period, today):
    def _cycle(**kwargs):
        day = kwargs.get('day', 1)

        # avg 30
        period.create(start_date='2026-01-01', end_date='2026-01-31')

        period.create(start_date=today(-(day - 1)), end_date=None)

        return user.obj.cycle_phase

    return _cycle


def test_user_cycle_phase_empty_property(user):
    assert user.obj.cycle_phase == 'no enough info'


def test_user_cycle_menstrual_phase_property(cycle_phase):
    assert cycle_phase(day=6) == 'menstrual'


def test_user_cycle_follicular_phase_property(cycle_phase):
    assert cycle_phase(day=18) == 'follicular'


def test_user_cycle_ovulation_window_phase_property(cycle_phase):
    assert cycle_phase(day=21) == 'ovulation window'


def test_user_cycle_luteal_phase_property(cycle_phase):
    assert cycle_phase(day=22) == 'luteal'
