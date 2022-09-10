import pytest

from music import create_app
from music.adapters import memory_repository
from music.adapters.memory_repository import MemoryRepository

from utils import get_project_root

TEST_DATA_PATH = get_project_root() / 'tests' / 'data'


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        # Path for loading test data into the repository.
        'TEST_DATA_PATH': TEST_DATA_PATH,
        # test_client will not send a CSRF token, so disable validation.
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='testuser', password='1234567890'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
