from pytest import mark

from api.tests import get_client, get_login, lorem, new_user

url = '/api/auth/token/'


def user_url():
    return url.replace('token', 'user')


def test_unprotected_route_empty_token():
    response = get_client('').get('/api/')
    assert response.status_code == 200


def test_unprotected_route_invalid_token():
    response = get_client().get('/api/')
    assert response.status_code == 200


@mark.django_db
def test_token_login_success():
    _, res, data = get_login()

    assert res.status_code == 200
    assert 'access' in data
    assert 'refresh' in data


@mark.django_db
def test_unprotected_route_valid_token():
    _, _, data = get_login()

    response = get_client(data['access']).get('/api/')
    assert response.status_code == 200


@mark.django_db
def test_token_login_invalid():
    def post_login(body):
        return get_client('').post(f'{url}login/', body)

    user = new_user()

    assert post_login({}).status_code == 400
    assert post_login({'username': lorem(15)}).status_code == 400
    assert (
        post_login(
            {
                'username': user.username,
                'password': lorem(15),
            }
        ).status_code
        == 401
    )


@mark.django_db
def test_token_refresh_success():
    _, _, data = get_login()

    response = get_client().post(f'{url}refresh/', {'refresh': data['refresh']})
    assert response.status_code == 200
    assert 'access' in response.json()


def test_token_refresh_invalid():
    response = get_client().post(f'{url}refresh/', {'refresh': lorem(255)})
    assert response.status_code == 401


@mark.django_db
def test_token_refresh_logout_success():
    _, _, data = get_login()

    response = get_client().post(f'{url}logout/', {'refresh': data['refresh']})
    assert response.status_code == 200

    response = get_client().post(f'{url}refresh/', {'refresh': data['refresh']})
    assert response.status_code == 401


@mark.django_db
def test_token_valid():
    _, _, data = get_login()

    response = get_client(data['access']).get(user_url())
    assert response.status_code == 200

    user = response.json()
    assert 'username' in user
    assert 'cycle_day' in user
    assert 'cycle_phase' in user


def test_protected_route_empty_token():
    assert get_client('').get(user_url()).status_code == 401


@mark.django_db
def test_protected_route_invalid_token():
    get_login()

    assert get_client().get(user_url()).status_code == 401
