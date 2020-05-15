BASE_URL = 'http://localhost:4433/api/v1/ls'


def test_get_source(client):
    response = client.get(BASE_URL + '/sources/1')
    print(response.json)
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "name": "CRUD app with mongo and flask",
        "description": "Okta developer explains how to create a simple CRUD app using flask, mongodb, docker-compose",
        "link": "https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react",
        "tags": [
            {
                "name": "python"
            },
            {
                "name": "js"
            },
            {
                "name": "flask"
            },
            {
                "name": "mongodb"
            },
            {
                "name": "react"
            },
            {
                "name": "full stack"
            }
        ],
        "created_at": "2020-05-10T17:16:43.572962",
        "last_updated": "2020-05-10T17:16:43.572962"
    }


def test_get_all_sources(client):
    response = client.get(BASE_URL + '/')
    assert response.status_code == 200
