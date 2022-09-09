import abc
from typing import List
from datetime import date

from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.playlist import PlayList

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        """ Returns the User with username 'username' from the repository. 

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, title: str) -> Track:
        """ Returns the Track with title from the repository.

        If there is no Track with the given title, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_album(self, title: str) -> Album:
        """ Returns the Album with title from the repository.

        If there is no Album with the given title, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist(self, name: str) -> Artist:
        """ Returns the Artist with name from the repository.

        If there is no Artist with the given name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, name: str) -> Genre:
        """ Returns the Genre with name from the repository.

        If there is no Genre with the given name, this method returns None.
        """
        raise NotImplementedError
