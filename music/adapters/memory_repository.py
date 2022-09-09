from typing import List

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

class MemoryRepository(AbstractRepository):
    
    def __init__(self):
        self.__users = list()
        self.__tracks = list()
        self.__albums = list()
        self.__artists = list()
        self.__genres = list()
        self.__reviews = list()
        self.__playlists = list()
        
    def add_user(self, user: User):
        self.__users.append(user)
    
    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
    
    def get_tracks_by_title(self, track_title: str) -> List[Track]:
        return [track for track in self.__tracks if track.title.lower() == track_title.strip().lower()]
    
    def get_tracks_by_artist(self, track_artist: str) -> List[Track]:
        return [track for track in self.__tracks if track.artist.full_name.lower() == track_artist.strip().lower()]
    
    def get_tracks_by_album(self, album_name: str) -> List[Track]:
        return [track for track in self.__tracks if track.album.title.lower() == album_name.strip().lower()]