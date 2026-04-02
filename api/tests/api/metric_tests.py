from pytest import mark

from api.tests import get_client, get_login, lorem, new_metric, new_option, new_user

url = '/api/metrics/'


@mark.django_db
def test_list_protected():
    assert get_client().get(url).status_code == 401

    assert get_client('').get(url).status_code == 401


@mark.django_db
def test_list():
    _, _, data = get_login()
    metric = new_metric()
    new_metric()

    res = get_client(data['access']).get(url)
    data = res.json()

    assert res.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    assert 'slug' in data[0]
    assert 'custom' in data[0]
    assert 'multiple' in data[0]
    assert any(i['slug'] == metric.slug for i in data)


@mark.django_db
def test_retrieve_protected():
    assert get_client().get(f'{url}{new_metric().slug}/').status_code == 401

    assert get_client('').get(f'{url}{new_metric().slug}/').status_code == 401


@mark.django_db
def test_retrieve():
    user, _, data = get_login()

    new_metric()
    metric = new_metric()

    new_option(metric, lorem(4), user)
    g_opt = new_option(metric, lorem(4))
    u_opt = new_option(metric, lorem(4), new_user())

    res = get_client(data['access']).get(f'{url}{metric.slug}/')
    data = res.json()

    assert res.status_code == 200
    assert isinstance(data, dict)

    assert 'slug' in data
    assert 'options' in data
    assert data['slug'] == metric.slug

    assert isinstance(data['options'], list)
    assert len(data['options']) == 2

    assert any(i['label'] == g_opt.label for i in data['options'])
    assert not any(i['label'] == u_opt.label for i in data['options'])


@mark.django_db
def test_not_found():
    new_metric()
    _, _, data = get_login()

    res = get_client(data['access']).get(f'{url}{lorem(4)}/')

    assert res.status_code == 404
