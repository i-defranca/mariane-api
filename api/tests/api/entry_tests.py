import pytest


@pytest.fixture
def basename():
    return '/api/entries/'


@pytest.fixture
def url(basename, today):
    return f'{basename}?month={today().year}-{today().month:02d}'


def test_list_required_param(api, basename):
    assert api.get(basename).status_code == 400
    assert api.get(f'{basename}?month=9090-90').status_code == 400


def test_list(api, url, entry, period, today, assert_list_size):
    month = today().month - 1 if today().month > 1 else 12
    entry.create(entry_date=f'{today().year}-{month:02d}-{today().day:02d}')

    assert_list_size(api.get(url), 0)

    period.create()
    entry.create()
    created_at = str(entry.create().created_at)[:10]

    data = assert_list_size(api.get(url), 2)

    assert 'metric' in data[0]
    assert 'option' in data[0]
    assert 'period' in data[0]
    assert 'entry_date' in data[0]
    assert 'created_at' in data[0]
    assert any(i['created_at'][:10] == created_at for i in data)

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
