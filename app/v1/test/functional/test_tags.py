BASE_URL = 'http://localhost:4433/api/v1/ls'


def test_get_tag(client):
    response = client.get(BASE_URL + "/tags")
    assert response.status_code == 200
