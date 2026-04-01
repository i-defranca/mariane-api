from pytest import mark

from api.tests import lorem, new_metric, new_option, new_user


@mark.django_db
def test_list(client):
    metric = new_metric()
    new_metric()

    response = client.get('/api/metrics/')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    assert 'slug' in data[0]
    assert 'custom' in data[0]
    assert 'multiple' in data[0]
    assert any(item['slug'] == metric.slug for item in data)


@mark.django_db
def test_retrieve(client):
    new_metric()
    user = new_user()
    metric = new_metric()
    new_option(metric, lorem(4))
    user_option = new_option(metric, lorem(4), user)
    global_option = new_option(metric, lorem(4))

    response = client.get(f'/api/metrics/{metric.slug}/')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, dict)

    assert 'slug' in data
    assert 'options' in data
    assert data['slug'] == metric.slug

    assert isinstance(data['options'], list)
    assert len(data['options']) == 2
    assert any(item['label'] == global_option.label for item in data['options'])
    assert not any(item['label'] == user_option.label for item in data['options'])


@mark.django_db
def test_not_found(client):
    new_metric()

    response = client.get(f'/api/metrics/{lorem(4)}/')

    assert response.status_code == 404
