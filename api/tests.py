import pytest
from pytest import mark

from .models import User


def test_api_health(client):
    response = client.get('/api/')
    assert response.status_code == 200


def create_user(username='username'):
    return User.objects.create_user(username=username)


@mark.django_db
def test_username_validation():
    with pytest.raises(ValueError):
        create_user(None)


@mark.django_db
def test_user_creation():
    assert str(create_user('username')) == 'username'
