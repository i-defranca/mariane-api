import pytest

from api.models import MetricOption as Option


@pytest.fixture
def url():
    return '/api/options/'


def test_list_now_allowed(api, url):
    assert api.get(url).status_code == 405


def test_update_now_allowed(api, url, option):
    assert api.patch(f'{url}{option.obj.pk}/').status_code == 405


def test_create(api, url, user, metric, lorem):
    body = {'metric': metric.obj.slug, 'label': (label := lorem(8))}

    assert (res := api.post(url, body)).status_code == 201
    data = res.json()

    obj = Option.objects.all().last()

    assert data['id'] == obj.pk
    assert data['label'] == label
    assert data['metric'] == metric.obj.slug
    assert obj.user.pk == user.obj.pk


def test_destroy(api, url, user, option):
    option.create()
    option.create(user=(other := user.create()))

    assert Option.objects.count() == 2
    assert Option.objects.filter(user=other).count() == 1

    assert api.delete(f'{url}{option.obj.pk}/').status_code == 204

    assert Option.objects.filter(user=other).count() == 1
    assert Option.objects.filter(pk=option.obj.pk).count() == 0
