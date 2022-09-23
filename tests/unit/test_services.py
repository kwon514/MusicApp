import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as auth_services
from music.playlist import services as playlist_services
from music.search import services as search_services


def test_can_add_user(in_memory_repo):
    new_user_name = 'user'
    new_password = 'Abcd123'
    auth_services.add_user(new_user_name, new_password, in_memory_repo)
    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'user'
    new_password = 'Abcd123'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False    

def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'user'
    new_password = 'Abcd123'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)        

def test_get_user(in_memory_repo):
    new_user_name = 'user'
    with pytest.raises(playlist_services.UnknownUserException):  
        playlist_services.get_user(new_user_name, in_memory_repo)

def test_get_playlists(in_memory_repo):
    new_user_name = 'user'
    with pytest.raises(playlist_services.UnknownUserException):  
        playlist_services.get_playlists(new_user_name, in_memory_repo) 

def test_add_playlist(in_memory_repo):
    playlist = "New Playlist"
    new_user_name = 'user'
    with pytest.raises(playlist_services.UnknownUserException):  
        playlist_services.add_playlist(playlist, new_user_name, in_memory_repo) 

def test_get_playlist_without_username(in_memory_repo):
    playlist = "New Playlist"
    new_user_name = 'user'
    with pytest.raises(playlist_services.UnknownUserException):  
        playlist_services.add_playlist(playlist, new_user_name, in_memory_repo)

def test_get_track_by_id(in_memory_repo):
    track_id = 2
    assert playlist_services.get_track_by_id(track_id, in_memory_repo).title == "Food"   

def test_get_tracks(in_memory_repo):
    title = "food"    
    assert search_services.get_tracks(title, in_memory_repo)[0].title == "Food"   

def test_get_artists(in_memory_repo):
    artist = "AWOL"    
    assert search_services.get_artists(artist, in_memory_repo)[0].title == "Food"

def test_get_albums(in_memory_repo):
    album = "AWOL - A Way Of Life"    
    assert search_services.get_albums(album, in_memory_repo)[0].title == "Food"   

def test_get_genres(in_memory_repo):
    genre = "Hip-Hop"    
    assert search_services.get_genres(genre, in_memory_repo)[0].title == "Food"         