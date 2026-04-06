import re

from django.conf import settings

PUBLIC = settings.PUBLIC_PATHS


def test_unprotected_route(api):
    url = next(filter(lambda s: re.search(r'^\^.*\$$', s), PUBLIC))
    if url:
        url = re.sub(r'[\^\$]', '', url)
        assert api.get(url).status_code == 200
        assert api.auth(False).get(url).status_code == 200


def test_auth_user_route(api):
    url = '/api/auth/user/'

    assert (res := api.get(url)).status_code == 200
    assert 'id' in res.json()
    assert 'username' in res.json()
    assert 'cycle_day' in res.json()
    assert 'cycle_phase' in res.json()

    assert api.auth(False).get(url).status_code == 401
