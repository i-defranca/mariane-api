import pytest

from api.models import Period


@pytest.fixture
def url():
    return '/api/periods/'


def test_list_required_param(api, url):
    assert api.get(url).status_code == 400
    assert api.get(f'{url}?month=9090-90').status_code == 400


def test_list(api, url, user, period, today, assert_list_size):
    month = today().month - 1 if today().month > 1 else 12
    param = f'{today().year}-{month:02d}'

    period.create(start_date=f'{param}-01', end_date=f'{param}-06')
    period.create(user=user.create())

    query = f'{url}?month={today().year}-{today().month:02d}'

    assert_list_size(api.get(query), 0)

    period.create()
    created = period.create(start_date=today(3), end_date=today(6))

    data = assert_list_size(api.get(query), 2)

    assert 'id' in data[0]
    assert 'start_date' in data[0]
    assert 'end_date' in data[0]
    assert 'created_at' in data[0]
    assert any(i['id'] == created.id for i in data)


def test_create(api, url, user, today):
    body = {'start_date': today(-5), 'end_date': today(-1)}

    assert (res := api.post(url, body)).status_code == 201
    data = res.json()

    obj = Period.objects.all().last()

    assert data['id'] == obj.pk
    assert data['start_date'] == today(-5).isoformat()
    assert data['end_date'] == today(-1).isoformat()
    assert obj.user.pk == user.obj.pk


def test_create_default_start(api, url, today):
    assert (res := api.post(url, {})).status_code == 201

    obj = Period.objects.all().last()

    assert res.json()['id'] == obj.pk
    assert obj.start_date == today()
