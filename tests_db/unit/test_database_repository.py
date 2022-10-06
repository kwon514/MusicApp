import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import RepositoryException


def test_add_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    repo.add_user(user)
    repo.add_user(User('Martin', '123456789'))
    user2 = repo.get_user('Dave')
    assert user2 == user and user2 is user


def test_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track = repo.get_track_by_id(2)
    repo.add_review(track, "This is a review", 3)
    review = repo.get_reviews_by_track(track)[0]
    assert review.review_text == "This is a review" and review.rating == 3


def test_get_reviews_by_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track = repo.get_track_by_id(2)
    repo.add_review(track, "This is a review", 3)
    repo.add_review(track, "This is a review too!", 2)
    reviews = repo.get_reviews_by_track(track)
    assert reviews[0].review_text == "This is a review" and reviews[0].rating == 3 and reviews[
        1].review_text == "This is a review too!" and reviews[1].rating == 2


def test_set_track_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track_list = [Track(10001, "TestTrackOne"), Track(10002, "TestTrackTwo")]
    repo.set_track_list(track_list)
    assert repo.get_track_by_id(10001).title == "TestTrackOne" and repo.get_track_by_id(
        10002).title == "TestTrackTwo"


def test_set_album_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    album_list = [Album(10001, "TestAlbumOne"), Album(10002, "TestAlbumTwo")]
    repo.set_album_list(album_list)
    with repo._session_cm as scm:
        album1 = scm.session.query(Album).filter(
            Album._Album__album_id == 10001).one()
        album2 = scm.session.query(Album).filter(
            Album._Album__album_id == 10002).one()
    assert album1.title == "TestAlbumOne" and album2.title == "TestAlbumTwo"


def test_set_artist_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    artist_list = [Artist(10001, "TestArtistOne"),
                   Artist(10002, "TestArtistTwo")]
    repo.set_artist_list(artist_list)
    with repo._session_cm as scm:
        artist1 = scm.session.query(Artist).filter(
            Artist._Artist__artist_id == 10001).one()
        artist2 = scm.session.query(Artist).filter(
            Artist._Artist__artist_id == 10002).one()
    assert artist1.full_name == "TestArtistOne" and artist2.full_name == "TestArtistTwo"


def test_set_genre_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre_list = [Genre(10001, "TestGenreOne"), Genre(10002, "TestGenreTwo")]
    repo.set_genre_list(genre_list)
    with repo._session_cm as scm:
        genre1 = scm.session.query(Genre).filter(
            Genre._Genre__genre_id == 10001).one()
        genre2 = scm.session.query(Genre).filter(
            Genre._Genre__genre_id == 10002).one()
    assert genre1.name == "TestGenreOne" and genre2.name == "TestGenreTwo"


def test_get_tracks_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    tracks = repo.get_tracks_by_title("Food")
    assert len(tracks) == 2 and "food" in tracks[0].title.lower(
    ) and "food" in tracks[1].title.lower()


def test_get_tracks_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    tracks = repo.get_tracks_by_artist("awol")
    assert len(tracks) == 4 and "awol" in tracks[0].artist.full_name.lower() and "awol" in tracks[1].artist.full_name.lower(
    ) and "awol" in tracks[2].artist.full_name.lower() and "awol" in tracks[3].artist.full_name.lower()


def test_get_tracks_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    tracks = repo.get_tracks_by_album("niris")
    count = 0
    for track in tracks:
        if "niris" in track.album.title.lower():
            count += 1
    assert count == len(tracks)


def test_get_tracks_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    tracks = repo.get_tracks_by_genre("avant-garde")
    count = 0
    for track in tracks:
        for genre in track.genres:
            if "avant-garde" in genre.name.lower():
                count += 1
    assert count == len(tracks)


def test_get_track_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track = Track(2, "Food")
    track_id = 2
    assert repo.get_track_by_id(track_id) == track


def test_add_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_playlist("TestPlaylist", User('Dave', '123456789'))
    assert repo.get_playlist("TestPlaylist").playlist_name == "TestPlaylist"


def test_get_playlists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    repo.add_playlist("TestPlaylist", user)
    repo.add_playlist("TestPlaylist2", user)
    retrieved_playlists = repo.get_playlists(user)
    assert len(
        retrieved_playlists) == 2 and retrieved_playlists[0].playlist_name == "TestPlaylist" and retrieved_playlists[1].playlist_name == "TestPlaylist2"


def test_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    track = repo._session_cm.session.query(Track).filter(
        Track._Track__title == "Electric Ave").one()
    repo.add_playlist("TestPlaylist", User('Dave', '123456789'))
    repo.add_track(track, "TestPlaylist")
    retrieved_tracks = repo.get_list_of_tracks("TestPlaylist")
    assert retrieved_tracks[0].title == "Electric Ave"


def test_get_list_of_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_playlist("TestPlaylist", User('Dave', '123456789'))
    track1 = repo._session_cm.session.query(Track).filter(
        Track._Track__title == "This World").one()
    track2 = repo._session_cm.session.query(Track).filter(
        Track._Track__title == "Electric Ave").one()
    repo.add_track(track1, "TestPlaylist")
    repo.add_track(track2, "TestPlaylist")
    playlist_tracks = repo.get_list_of_tracks("TestPlaylist")
    assert playlist_tracks[0].title == "This World" and playlist_tracks[1].title == "Electric Ave"
