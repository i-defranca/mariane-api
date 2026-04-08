import pytest


@pytest.fixture
def url():
    return '/api/metrics/'


def test_create_now_allowed(api, url):
    assert api.post(url, {}).status_code == 405


def test_list(api, url, metric, assert_list_size):
    metric.create()
    metric.create()

    data = assert_list_size(api.get(url), 2)

    assert 'slug' in data[0]
    assert 'custom' in data[0]
    assert 'multiple' in data[0]
    assert any(i['slug'] == metric.obj.slug for i in data)


def test_retrieve(api, url, user, metric, option):
    metric.create()
    metric.create()
    option.create()
    g_opt = option.create(user=None)
    u_opt = option.create(user=user.create())

    assert g_opt.user is None
    assert u_opt.user.pk != user.obj.pk
    assert option.obj.user.pk == user.obj.pk

    data = (res := api.get(f'{url}{metric.obj.slug}/')).json()

    assert res.status_code == 200
    assert isinstance(data, dict)

    assert 'slug' in data
    assert 'custom' in data
    assert 'multiple' in data
    assert data['slug'] == metric.obj.slug

    assert 'options' in data
    assert isinstance(data['options'], list)
    assert len(data['options']) == 2

    assert any(i == g_opt.label for i in data['options'])
    assert any(i == option.obj.label for i in data['options'])

    assert not any(i == u_opt.label for i in data['options'])
