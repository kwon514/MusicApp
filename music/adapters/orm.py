from time import time
from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

tracks_table = Table(
    'tracks', metadata,
    Column('track_id', Integer, primary_key=True, autoincrement=True),
    Column('track_title', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.artist_id')),
    Column('album_id', ForeignKey('albums.album_id')),
    Column('track_url', String(255), nullable=False),
    Column('track_duration', Integer, nullable=False),
    Column('rating', Integer)
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('review_text', String(255), nullable=False),
    Column('rating', Integer),
    Column('timestamp', DateTime, nullable=False)
)

playlists_table = Table(
    'playlists', metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_name', String(255), nullable=False),
    Column('user_id', ForeignKey('users.id'))
)

genres_table = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

artists_table = Table(
    'artists', metadata,
    Column('artist_id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

albums_table = Table(
    'albums', metadata,
    Column('album_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('album_url', String(255), nullable=False),
    Column('album_type', String(255), nullable=False),
    Column('release_year', Integer)
)

track_genre_table = Table(
    'track_genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

playlist_track_table = Table(
    'playlist_track', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlists.playlist_id')),
    Column('track_id', ForeignKey('tracks.track_id'))
)

def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__playlists': relationship(PlayList, back_populates='_PlayList__user'),
    })

    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.track_title,
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__track_duration': tracks_table.c.track_duration,
        '_Track__rating': tracks_table.c.rating,
        '_Track__artist': relationship(Artist, back_populates='_Artist__tracks'),
        '_Track__genres': relationship(Genre, secondary=track_genre_table, back_populates='_Genre__tracks'),
        '_Track__playlists': relationship(PlayList, secondary=playlist_track_table, back_populates='_PlayList__list_of_tracks'),
        '_Track__reviews': relationship(Review, back_populates='_Review__track')
    })

    mapper(Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__track': relationship(Track, back_populates='_Track__reviews')
    })

    mapper(PlayList, playlists_table, properties={
        '_PlayList__playlist_name': playlists_table.c.playlist_name,
        '_PlayList__list_of_tracks': relationship(Track, secondary=playlist_track_table, back_populates='_Track__playlists'),
        '_PlayList__user': relationship(User, back_populates='_User__playlists')
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name,
        '_Genre__tracks': relationship(Track, secondary=track_genre_table, back_populates='_Track__genres')
    })

    mapper(Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name,
        '_Artist__tracks': relationship(Track, back_populates='_Track__artist')
    })

    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
        '_Album__album_url': albums_table.c.album_url,
        '_Album__album_type': albums_table.c.album_type,
        '_Album__release_year': albums_table.c.release_year,
        '_Album__tracks': relationship(Track, backref='_Track__album')
    })
