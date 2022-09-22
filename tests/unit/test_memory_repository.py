from typing import List

import pytest

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import RepositoryException


def test_add_user(in_memory_repo):
    user = User('dave', '123456789', 1)
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user  

def test_get_tracks_by_title(in_memory_repo):
    title = "food"    
    in_memory_repo.get_tracks_by_title(title)

def test_get_tracks_by_artists(in_memory_repo):
    artist = "AWOL"    
    in_memory_repo.get_tracks_by_artist(artist)

def test_get_tracks_by_albums(in_memory_repo):
    album = "AWOL - A Way Of Life"    
    in_memory_repo.get_tracks_by_album(album)   

def test_get_track_by_genres(in_memory_repo):
    genre = "Rock"    
    in_memory_repo.get_tracks_by_genre(genre)   

def test_get_track_by_id(in_memory_repo):
    track_id = 2
    in_memory_repo.get_track_by_id(track_id)   

def test_add_playlist(in_memory_repo):
    user = User('dave', '123456789', 1)
    in_memory_repo.add_playlist("New Playlist", user)

def test_get_playlist(in_memory_repo):
    playlist_name = "playlist_name"
    in_memory_repo.get_playlist(playlist_name) 
  