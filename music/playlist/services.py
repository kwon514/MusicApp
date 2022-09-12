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



def get_playlists(repo: AbstractRepository):
    return repo.get_playlists()

def add_playlist(playlist_name: str, repo: AbstractRepository):    
    # Check that the given user name is available.
    playlist = repo.get_playlist(playlist_name)
    if playlist is not None:
        raise PlaylistNotUniqueException

    # Create and store the new User, with password encrypted.
    playlist = PlayList(playlist_name)
    repo.add_playlist(playlist)