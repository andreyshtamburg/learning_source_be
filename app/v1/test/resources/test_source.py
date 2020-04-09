def test_get_source(client):
    response = client.get('http://localhost:4433/api/v1/ls/sources/1')
    print(response.json)
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "name": "CRUD app with mongo and flask",
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
        "created_at": "2020-04-05T14:46:04.575686",
        "last_updated": "2020-04-05T14:46:04.575686"
    }


def test_create_resource(client):
    pass
