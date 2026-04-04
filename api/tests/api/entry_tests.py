from datetime import date, datetime

from pytest import mark

from api.tests import get_client, get_login, new_entry, new_period

base = '/api/entries/'

today = date.today()
url = f'{base}?month={today.year}-{today.month:02d}'


@mark.django_db
def test_list_protected():
    assert get_client().get(url).status_code == 401

    assert get_client('').get(url).status_code == 401


@mark.django_db
def test_list_required_month_param():
    _, _, data = get_login()

    assert get_client(data['access']).get(base).status_code == 400


@mark.django_db
def test_list_bad_month_param():
    _, _, data = get_login()

    assert get_client(data['access']).get(f'{base}?month=9090-90').status_code == 400


@mark.django_db
def test_list_month_filter_empty_result():
    user, _, data = get_login()
    month = today.month - 1 if today.month > 1 else 12
    new_entry(user, entry_date=date(today.year, month, today.day))

    res = get_client(data['access']).get(url)
    data = res.json()

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0


def setup_entry_and_login(period=True):
    user, _, data = get_login()

    if period:
        new_period(user)

    entry = new_entry(user)
    new_entry(user)

    return entry, data['access']


def get_url(token, url):
    res = get_client(token).get(url)

    return res, res.json()


@mark.django_db
def test_list_month_filter():
    entry, token = setup_entry_and_login()
    period = entry.period

    res, data = get_url(token, url)

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    assert 'metric' in data[0]
    assert 'option' in data[0]
    assert 'period' in data[0]
    assert 'entry_date' in data[0]
    assert 'created_at' in data[0]
    assert any(
        datetime.fromisoformat(i['created_at']) == entry.created_at for i in data
    )

    assert isinstance(data[0]['period'], dict)
    assert 'start_date' in data[0]['period']
    assert 'end_date' in data[0]['period']

    assert data[0]['period']['start_date'] == str(period.start_date)
    assert data[0]['period']['end_date'] == str(period.end_date)


@mark.django_db
def test_list_month_and_period_filter():
    _, token = setup_entry_and_login()

    res, data = get_url(token, f'{url}&period=false')

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

    res, data = get_url(token, f'{url}&period=true')

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    _, token = setup_entry_and_login(period=False)

    res, data = get_url(token, f'{url}&period=false')

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    res, data = get_url(token, f'{url}&period=true')

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0
