def test_api_health(client):
    response = client.get('/api/')
    assert response.status_code == 200
