import pytest

from api.models import Entry


@pytest.fixture
def basename():
    return '/api/entries/'


@pytest.fixture
def url(basename, today):
    return f'{basename}?month={today().year}-{today().month:02d}'


def test_retrieve_now_allowed(api, basename, entry):
    assert api.get(f'{basename}{entry.obj.pk}/').status_code == 405


def test_update_now_allowed(api, basename, entry):
    assert api.patch(f'{basename}{entry.obj.pk}/').status_code == 405


def test_list_required_param(api, basename):
    assert api.get(basename).status_code == 400
    assert api.get(f'{basename}?month=9090-90').status_code == 400


def test_list(api, url, entry, user, period, today, assert_list_size):
    month = today().month - 1 if today().month > 1 else 12
    entry.create(entry_date=f'{today().year}-{month:02d}-{today().day:02d}')

    entry.create(user=user.create())

    assert_list_size(api.get(url), 0)

    period.create()
    entry.create()
    created = entry.create()

    data = assert_list_size(api.get(url), 2)

    assert 'id' in data[0]
    assert 'metric' in data[0]
    assert 'option' in data[0]
    assert 'period' in data[0]
    assert 'entry_date' in data[0]
    assert 'created_at' in data[0]
    assert any(i['id'] == created.id for i in data)

    assert isinstance(data[0]['period'], dict)
    assert 'end_date' in data[0]['period']
    assert 'start_date' in data[0]['period']

    assert data[0]['period']['end_date'] == str(period.obj.end_date)
    assert data[0]['period']['start_date'] == str(period.obj.start_date)


def test_list_period_filter(api, url, entry, period, assert_list_size):
    entry.create()
    entry.create()

    assert_list_size(api.get(f'{url}&period=false'), 2)

    assert_list_size(api.get(f'{url}&period=true'), 0)

    period.create()

    assert_list_size(api.get(f'{url}&period=false'), 0)

    assert_list_size(api.get(f'{url}&period=true'), 2)


def test_create(api, basename, user, metric, option, period, today):
    period.create()

    body = {'metric': metric.obj.slug, 'option': option.obj.label}
    res = api.post(basename, body)

    assert res.status_code == 201
    data = res.json()

    assert data['id'] == metric.obj.pk
    assert data['metric'] == metric.obj.slug
    assert data['option'] == option.obj.label
    assert data['entry_date'] == today().isoformat()
    assert data['period']['end_date'] == str(period.obj.end_date)
    assert data['period']['start_date'] == str(period.obj.start_date)

    last = Entry.objects.all().last()

    assert last.user.pk == user.obj.pk


def test_destroy(api, basename, user, entry):
    entry.create()
    entry.create(user=(other := user.create()))

    assert Entry.objects.count() == 2
    assert Entry.objects.filter(user=other).count() == 1

    assert api.delete(f'{basename}{entry.obj.pk}/').status_code == 204

    assert Entry.objects.filter(user=other).count() == 1
    assert Entry.objects.filter(pk=entry.obj.pk).count() == 0
