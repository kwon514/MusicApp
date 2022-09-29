from typing import List

from sqlalchemy import desc, asc, func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user   
        
    def set_track_list(self, track_list: list):
        with self._session_cm as scm:
            for track in track_list:
                scm.session.add(track)
                scm.commit() 

    def set_album_list(self, album_list: list):
        with self._session_cm as scm:
            for album in album_list:
                scm.session.add(album)
                scm.commit() 

    def set_genre_list(self, genre_list: list):
        with self._session_cm as scm:
            for genre in genre_list:
                scm.session.add(genre)
                scm.commit()                   

    def set_artist_list(self, artist_list: list):
        with self._session_cm as scm:
            for artist in artist_list:
                scm.session.add(artist)
                scm.commit()               

    def get_tracks_by_title(self, track_title: str) -> List[Track]:
        return self._session_cm.session.query(Track).filter(func.lower(Track._Track__title) == track_title).all()
 
    def get_tracks_by_artist(self, track_artist: str) -> List[Track]:
        artist = self._session_cm.session.query(Artist).filter(func.lower(Artist._Artist__full_name) == func.lower(track_artist)).first()
        return self._session_cm.session.query(Track).filter(Track._Track__artist.__eq__(artist)).all()

    def get_tracks_by_album(self, album_name: str) -> List[Track]:
        tracks = []
        try:
            album = self._session_cm.session.query(Album).filter(func.lower(Album._Album__title) == func.lower(album_name)).one()
            tracks = self._session_cm.session.query(Track).filter(Track._Track__album.__eq__(album)).all()
        except:
            pass    
        return tracks

    def get_tracks_by_genre(self, genre_name: str) -> List[Track]:
        track_ids = []
        track_list = []
        try:
            row = self._session_cm.session.execute('SELECT genre_id FROM genres WHERE name = :name', {'name': genre_name}).fetchone() 
            genre_id = row[0]
            track_ids = self._session_cm.session.execute(
                        'SELECT track_id FROM track_genre WHERE genre_id = :genre_id',
                        {'genre_id': genre_id}).fetchall()  
            for id in track_ids:
                track_list.append(self._session_cm.session.query(Track).filter(Track._Track__track_id == id[0]).one())
        except:
            pass          
        return track_list   