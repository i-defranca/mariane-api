import pytest
from rest_framework.test import APIClient


class APIAuth(APIClient):
    def __init__(self, *args, access, refresh, **kwargs):
        self._auth = True
        self._access = access
        self._refresh = refresh
        super().__init__(*args, **kwargs)

    def _setup(self):
        if self._auth:
            header = f'Bearer {self._access}'
            self.credentials(HTTP_AUTHORIZATION=header)

    def auth(self, token=None):
        if token is not None:
            self._access = token
        return self

    def request(self, **kwargs):
        self._setup()
        return super().request(**kwargs)


@pytest.fixture
def api(user):
    body = {
        'username': user.obj.username,
        'password': user.obj.raw_password,
    }
    data = APIClient().post('/api/auth/token/login/', body).json()

    return APIAuth(access=data.get('access'), refresh=data.get('refresh'))


@pytest.fixture
def assert_list_size():
    def _assert(res, size):
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) == size

        return res.json()

    return _assert
