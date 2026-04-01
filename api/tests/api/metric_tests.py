from pytest import mark

from api.tests import lorem, new_metric


@mark.django_db
def test_index(client):
    metric = new_metric()
    new_metric()

    response = client.get('/api/metrics/')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    assert 'id' in data[0]
    assert 'slug' in data[0]
    assert any(item['slug'] == metric.slug for item in data)


@mark.django_db
def test_get(client):
    new_metric()
    metric = new_metric()

    response = client.get(f'/api/metrics/{metric.slug}/')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, dict)

    assert 'id' in data
    assert 'slug' in data
    assert data['id'] == metric.id


@mark.django_db
def test_not_found(client):
    new_metric()

    response = client.get(f'/api/metrics/{lorem(4)}/')

    assert response.status_code == 404
