from typing import List
import csv
from pathlib import Path
from music.adapters import csvdatareader

from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader
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

    def add_review(self, review: Review):
        self.__reviews.append(review)
        
    def get_reviews_by_track(self, track: Track) -> List[Review]:
        return [review for review in self.__reviews if review.track == track]

    def set_track_list(self, track_list: list):
        self.__tracks += track_list

    def set_album_list(self, album_list: list):
        self.__albums += album_list

    def set_artist_list(self, artist_list: list):
        self.__artists += artist_list

    def set_genre_list(self, genre_list: list):
        self.__genres += genre_list

    def get_tracks_by_title(self, track_title: str) -> List[Track]:
        return [track for track in self.__tracks if track.title.lower()[0:len(track_title)] == track_title.strip().lower()[0:len(track_title)]]

    def get_tracks_by_artist(self, track_artist: str) -> List[Track]:
        return [track for track in self.__tracks if track.artist.full_name.lower()[0:len(track_artist)] == track_artist.strip().lower()[0:len(track_artist)]]

    def get_tracks_by_album(self, album_name: str) -> List[Track]:
        results = []
        for track in self.__tracks:
            try:
                if track.album.title.lower()[0:len(album_name)] == album_name.strip().lower()[0:len(album_name)]:
                    results.append(track)
            except AttributeError:
                pass
        return results

    def get_tracks_by_genre(self, genre_name: str) -> List[Track]:
        results = []
        for track in self.__tracks:
            try:
                for genre in track.genres:
                    if genre.name.lower()[0:len(genre_name)] == genre_name.strip().lower()[0:len(genre_name)]:
                        results.append(track)
            except AttributeError:
                pass
        return results            

    def get_track_by_id(self, track_id: int) -> Track:
        for track in self.__tracks:
            if int(track.track_id) == track_id:
                return track 

    def add_playlist(self, playlist_name: str, user: User):
        playlist = PlayList(playlist_name, user)
        self.__playlists.append(playlist)

    def get_playlist(self, playlist_name) -> PlayList:
        return next((playlist for playlist in self.__playlists if playlist.playlist_name == playlist_name), None)

    def get_playlists(self, user) -> List[PlayList]:
        return [playlist for playlist in self.__playlists if playlist.user == user]

    def add_track(self, track, playlist_name: str):
        list_of_tracks = self.get_list_of_tracks(playlist_name)   
        list_of_tracks.append(track)
 
    def get_list_of_tracks(self, playlist_name: str) -> List[Track]:
        playlist = self.get_playlist(playlist_name)
        list_of_tracks = playlist.list_of_tracks()     
        return list_of_tracks

def populate(data_path: Path, repo: MemoryRepository):
    file_data = TrackCSVReader(str(Path(data_path) / 'raw_albums_excerpt.csv'), str(Path(data_path) / 'raw_tracks_excerpt.csv'))
    file_data.read_csv_files()
    repo.set_track_list(file_data.dataset_of_tracks)
    repo.set_album_list(file_data.dataset_of_albums)
    repo.set_genre_list(file_data.dataset_of_genres)

   