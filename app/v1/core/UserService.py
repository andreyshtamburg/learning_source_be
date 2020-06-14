import requests

USER_SOURCE_URL = 'http://host.docker.internal:5533'


def call_get(endpoint):
    return requests.get(USER_SOURCE_URL + endpoint)


def verify_auth_token(token):
    auth_header = {'Authorization': token}
    print(f'{auth_header}=')
    response = requests.post(USER_SOURCE_URL+"/api/v1/auth/token_valid", headers=auth_header).json()
    print(f'{response}=')
    return response
