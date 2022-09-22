from typing import List, Iterable

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList


class PlaylistNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user


def get_playlists(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return repo.get_playlists(user)


def add_playlist(playlist_name: str, user_name: str, repo: AbstractRepository):
    playlist = repo.get_playlist(playlist_name)
    if playlist is not None:
        raise PlaylistNotUniqueException
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    repo.add_playlist(playlist_name, user)


def get_playlist(playlist_name: str, user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    playlist = repo.get_playlist(playlist_name)
    return playlist


def get_playlist_without_username(playlist_name: str, repo: AbstractRepository):
    playlist = repo.get_playlist(playlist_name)
    return playlist


def add_track(track: Track, playlist_name: str, repo: AbstractRepository):
    repo.add_track(track, playlist_name)


def get_track_by_id(track_id: int, repo: AbstractRepository):
    return repo.get_track_by_id(track_id)


def get_list_of_tracks(playlist_name: str, repo: AbstractRepository):
    return repo.get_list_of_tracks(playlist_name)


def create_playlist_from_list(playlist_name: str, list_of_tracks: List[Track], user_name: str, repo: AbstractRepository):
    playlist_copy_name = "Copy of " + playlist_name
    playlist = repo.get_playlist(playlist_copy_name)
    if playlist is not None:
        raise PlaylistNotUniqueException
    user = repo.get_user(user_name)
    repo.add_playlist(playlist_copy_name, user)
    for track in list_of_tracks:
        repo.add_track(track, playlist_copy_name)
