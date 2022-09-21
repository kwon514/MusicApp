import pytest

from flask import session


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    response = client.post(
        '/authentication/register',
        data={'user_name': 'user1234567', 'password': 'User1234567'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client):
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_name' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Explore a new world of music.' in response.data


def test_login_required_to_create_playlist(client):
    response = client.post('/create_playlist')
    assert response.headers['Location'] == '/authentication/login'

def test_search(client):
    response = client.get('/search')
    assert response.status_code == 200

    