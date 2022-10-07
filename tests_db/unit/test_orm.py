import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

review_timestamp = datetime.datetime(2020, 12, 30, 1, 1, 1)


def insert_user(empty_session, values=None):
    new_id = 1
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_id = values[0]
        new_name = values[1]
        new_password = values[2]

    empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                          {'id': new_id, 'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where id = :id',
                                {'id': new_id}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                              {'id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_artist(empty_session):
    empty_session.execute(
        'INSERT INTO artists (artist_id, full_name) VALUES (1, "ExampleArtist")')
    row = empty_session.execute('SELECT artist_id from artists').fetchone()
    return row[0]


def insert_album(empty_session):
    empty_session.execute(
        'INSERT INTO albums (album_id, title, album_url, album_type, release_year) VALUES (1, "ExampleAlbum", "www.examplealbum.com", "Album", 2020)')
    row = empty_session.execute(
        'SELECT album_id from albums where album_id = 1').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_id, name) VALUES (1, "ExampleGenre")')
    rows = list(empty_session.execute('SELECT genre_id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (track_id, track_title, track_url, track_duration, rating) VALUES (1, "ExampleTrack", "www.exampletrack.com", 100, 3)')
    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]


def insert_track_review(empty_session):
    track_key = insert_track(empty_session)
    timestamp = datetime.datetime.now()
    empty_session.execute(
        'INSERT INTO reviews (review_id, track_id, review_text, rating, timestamp) VALUES '
        '(1, :track_id, "This is an example review...", 3, :timestamp)',
        {'track_id': track_key, 'timestamp': timestamp}
    )
    row = empty_session.execute(
        'SELECT review_id from reviews where review_id = 1').fetchone()
    return row[0]


def insert_playlist(empty_session):
    user_key = insert_user(empty_session)
    empty_session.execute('INSERT INTO playlists (playlist_id, playlist_name, user_id) VALUES (1, "ExamplePlaylist", :user_id)',
                          {'user_id': user_key}
                          )
    row = empty_session.execute('SELECT playlist_id from playlists').fetchone()
    return row[0]


def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genre (track_id, genre_id) VALUES (:track_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(
            stmt, {'track_id': track_key, 'genre_id': genre_key})


def insert_playlist_track_associations(empty_session, playlist_key, track_keys):
    stmt = 'INSERT INTO playlist_track (playlist_id, track_id) VALUES (:playlist_id, :track_id)'
    for track_key in track_keys:
        empty_session.execute(
            stmt, {'playlist_id': playlist_key, 'track_id': track_key})


def make_user():
    user = User("Andrew", "1234567", 1)
    return user


def make_artist():
    artist = Artist(1, "ExampleArtist")
    return artist


def make_album():
    album = Album(1, "ExampleAlbum")
    album.album_url = "www.examplealbum.com"
    album.album_type = "Album"
    album.release_year = 2020
    return album


def make_genre():
    genre = Genre(1, "ExampleGenre")
    return genre


def make_track():
    track = Track(1, "ExampleTrack")
    track.track_url = "www.exampletrack.com"
    track.track_duration = 100
    track.rating = 3
    return track


def make_review(track: Track, review_text: str, rating: int):
    review = Review(track, review_text, rating)
    return review


def make_playlist(user: User):
    playlist = PlayList("ExamplePlaylist", user)
    return playlist

def make_playlist_track_association(playlist: PlayList, track: Track):
    if track in playlist.list_of_tracks:
        raise ValueError("Track is already in the playlist.")
    playlist.add_track(track)

def make_track_genre_association(track: Track, genre: Genre):
    if genre in track.genres:
        raise ValueError("Genre is already associated with track.")
    track.add_genre(genre)


def test_loading_of_users(empty_session):
    users = list()
    users.append((1, "Andrew", "1234567"))
    users.append((2, "Cindy", "7654321"))
    insert_users(empty_session, users)
    expected_users = [
        User("Andrew", "1234567", 1),
        User("Cindy", "7654321", 2)
    ]
    assert empty_session.query(User).all() == expected_users


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "1234567")]


def test_saving_of_users_with_common_user_id(empty_session):
    insert_user(empty_session, (1, "Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "1234567", 1)
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_albums(empty_session):
    album_key = insert_album(empty_session)
    expected_album = make_album()
    fetched_album = empty_session.query(Album).one()
    assert expected_album == fetched_album
    assert album_key == fetched_album.album_id


def test_loading_of_artists(empty_session):
    artist_key = insert_artist(empty_session)
    expected_artist = make_artist()
    fetched_artist = empty_session.query(Artist).one()
    assert expected_artist == fetched_artist
    assert artist_key == fetched_artist.artist_id


def test_loading_of_playlists(empty_session):
    user = make_user()
    playlist_key = insert_playlist(empty_session)
    fetched_playlist = empty_session.query(PlayList).one()
    assert playlist_key == fetched_playlist.playlist_id


def test_loading_of_playlist_tracks(empty_session):
    playlist_key = insert_playlist(empty_session)
    track_keys = [insert_track(empty_session)]
    insert_playlist_track_associations(empty_session, playlist_key, track_keys)

    playlist = empty_session.query(PlayList).get(playlist_key)
    tracks = [empty_session.query(Track).get(track_key)
              for track_key in track_keys]

    for track in tracks:
        assert track in playlist.list_of_tracks


def test_loading_of_tracks(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()
    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id


def test_loading_of_track_reviews(empty_session):
    review_key = insert_track_review(empty_session)
    fetched_review = empty_session.query(Review).one()
    assert review_key == fetched_review.review_id


def test_loading_of_track_genres(empty_session):
    track_key = insert_track(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_track_genre_associations(empty_session, track_key, genre_keys)

    track = empty_session.query(Track).get(track_key)
    genres = [empty_session.query(Genre).get(genre_key)
              for genre_key in genre_keys]

    for genre in genres:
        assert genre in track.genres

def test_saving_of_album(empty_session):
    album = make_album()
    empty_session.add(album)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT title, album_url, album_type, release_year FROM albums'))
    assert rows == [("ExampleAlbum", "www.examplealbum.com", "Album", 2020)]


def test_saving_of_artist(empty_session):
    artist = make_artist()
    empty_session.add(artist)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT full_name FROM artists'))
    assert rows == [('ExampleArtist',)]


def test_saving_of_playlist_track(empty_session):
    user = make_user()
    playlist = make_playlist(user)
    track = make_track()
    make_playlist_track_association(playlist, track)
    empty_session.add(playlist)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT playlist_id FROM playlists'))
    playlist_key = rows[0][0]
    
    # Check that the tracks table has a new record.
    rows = list(empty_session.execute('SELECT track_id, track_title FROM tracks'))
    track_key = rows[0][0]
    assert rows[0][1] == "ExampleTrack"
    
    # Check that the playlist_track table has a new record.
    rows = list(empty_session.execute('SELECT playlist_id, track_id FROM playlist_track'))
    playlist_foreign_key = rows[0][0]
    track_foreign_key = rows[0][1]
    
    assert playlist_key == playlist_foreign_key
    assert track_key == track_foreign_key

def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT track_title, track_url, track_duration, rating FROM tracks'))
    assert rows == [("ExampleTrack", "www.exampletrack.com", 100, 3)]


def test_saving_of_track_review(empty_session):
    track = make_track()
    
    review_text = "This is an example review..."
    rating = 3
    review = make_review(track, review_text, rating)
    empty_session.add(review)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT review_id FROM reviews'))
    review_key = rows[0][0]
    
    rows = list(empty_session.execute('SELECT track_id, review_text, rating FROM reviews'))
    assert rows == [(review_key, review_text, rating)]
    

def test_saving_of_track_genre(empty_session):
    track = make_track()
    genre = make_genre()
    make_track_genre_association(track, genre)
    empty_session.add(track)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT track_id FROM tracks'))
    track_key = rows[0][0]
    
    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT genre_id, name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][1] == "ExampleGenre"
    
    # Check that the track_genre table has a new record.
    rows = list(empty_session.execute('SELECT track_id, genre_id FROM track_genre'))
    track_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]
    
    assert track_key == track_foreign_key
    assert genre_key == genre_foreign_key
