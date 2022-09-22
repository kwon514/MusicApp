from typing import List, Iterable

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

class UnknownUserException(Exception):
    pass

def get_track_by_id(track_id: int, repo: AbstractRepository):
    return repo.get_track_by_id(track_id)

def add_review(review: Review, repo: AbstractRepository):
    repo.add_review(review)

def get_review(track: Track, repo: AbstractRepository):
    return repo.get_reviews_by_track(track)

def get_playlists(user_name: str,repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return repo.get_playlists(user)