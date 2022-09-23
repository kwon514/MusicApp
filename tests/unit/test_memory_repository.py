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
    track = Track(2, "Food")
    title = "Food"    
    assert in_memory_repo.get_tracks_by_title(title)[0] == track

def test_get_tracks_by_artists(in_memory_repo):
    track = Track(2, "Food")
    artist = "AWOL"    
    assert in_memory_repo.get_tracks_by_artist(artist)[0] == track

def test_get_tracks_by_albums(in_memory_repo):
    track = Track(2, "Food")
    album = "AWOL - A Way Of Life"    
    assert in_memory_repo.get_tracks_by_album(album)[0] == track   

def test_get_track_by_genres(in_memory_repo):
    track = Track(2, "Food")
    genre = "Hip-Hop"    
    assert in_memory_repo.get_tracks_by_genre(genre)[0] == track   

def test_get_track_by_id(in_memory_repo):
    track = Track(2, "Food")
    track_id = 2
    assert in_memory_repo.get_track_by_id(track_id) == track   

def test_add_playlist(in_memory_repo):
    user = User('dave', '123456789', 1)
    in_memory_repo.add_playlist("New Playlist", user)
    assert in_memory_repo.get_playlists(user)[0].playlist_name == "New Playlist"

def test_get_playlist(in_memory_repo):
    user = User('dave', '123456789', 1)
    playlist = PlayList("New Playlist", user)
    in_memory_repo.add_playlist("New Playlist", user)
    playlist = in_memory_repo.get_playlists(user)[0]
    assert in_memory_repo.get_playlist("New Playlist") == playlist

  