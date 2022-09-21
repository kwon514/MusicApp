from typing import List, Iterable

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

def get_tracks(track_name: str, repo: AbstractRepository):
    return repo.get_tracks_by_title(track_name)

def get_artists(artist_name: str, repo: AbstractRepository):
    return repo.get_tracks_by_artist(artist_name)

def get_albums(album_name: str, repo: AbstractRepository):
    return repo.get_tracks_by_album(album_name)

def get_genres(genre_name: str, repo: AbstractRepository):
    return repo.get_tracks_by_genre(genre_name)    