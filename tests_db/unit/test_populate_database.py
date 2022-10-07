from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'artists', 'genres', 'playlist_track', 'playlists', 'reviews', 'track_genre', 'tracks', 'users']

def test_database_populate_select_all_albums(database_engine):
    
    # Get table information
    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_album_names = []
        for row in result:
            all_album_names.append(row['title'])

        assert all_album_names == ['AWOL - A Way Of Life', 'Niris', 'Constant Hitmaker', 'Live at LACE', 'Every Man For Himself']
        
def test_database_populate_select_all_artists(database_engine):
    
    # Get table information
    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)

        all_artist_names = []
        for row in result:
            all_artist_names.append(row['full_name'])

        assert all_artist_names == ['AWOL', 'Nicky Cook', 'Kurt Vile', 'Airway', 'Alec K. Redfearn & the Eyesores']
        
def test_database_populate_select_all_genres(database_engine):
    
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]
    
    
    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['name'])

        assert all_genre_names == ['Avant-Garde', 'Pop', 'Folk', 'Hip-Hop', 'Noise', 'Experimental Pop', 'Singer-Songwriter']

def test_database_populate_select_all_tracks(database_engine):
    
    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_track_names = []
        for row in result:
            all_track_names.append(row['track_title'])

        assert all_track_names == ['Food', 'Electric Ave', 'This World', 'Freeway', 'Spiritual Level', 'Too Happy', 'Street Music', 'Side A', 'Side B', 'CandyAss']