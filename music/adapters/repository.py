import abc
from typing import List
from datetime import date

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        raise NotImplementedError 

    # @abc.abstractmethod
    # def add_review(self, review: Review):
    #     raise NotImplementedError
    
    # @abc.abstractmethod
    # def get_reviews_by_track(self, track: Track) -> List[Review]:
    #     raise NotImplementedError

    @abc.abstractmethod
    def set_track_list(self, track_list: list):
        raise NotImplementedError
    
    @abc.abstractmethod
    def set_album_list(self, album_list: list):
        raise NotImplementedError

    @abc.abstractmethod
    def set_artist_list(self, artist_list: list):
        raise NotImplementedError

    @abc.abstractmethod
    def set_genre_list(self, genre_list: list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_title(self, track_title: str) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artist(self, track_artist: str) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, album_name: str) -> List[Track]:
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_tracks_by_genre(self, genre_name: str) -> List[Track]:
    #     raise NotImplementedError    

    # @abc.abstractmethod
    # def get_track_by_id(self, track_id: int) -> Track:
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def add_playlist(self, playlist_name: str, user: User):
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_playlist(self, playlist_name: str) -> PlayList:
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_playlists(self, user) -> List[PlayList]:
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def add_track(self, track: Track, playlist_name: str):
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_list_of_tracks(self, playlist_name: str) -> List[Track]:
    #     raise NotImplementedError

