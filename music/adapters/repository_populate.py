from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    file_data = TrackCSVReader(str(Path(data_path) / 'raw_albums_excerpt.csv'), str(Path(data_path) / 'raw_tracks_excerpt.csv'))
    file_data.read_csv_files()
    repo.set_track_list(file_data.dataset_of_tracks)
    repo.set_album_list(file_data.dataset_of_albums)
    repo.set_genre_list(file_data.dataset_of_genres)
    repo.set_artist_list(file_data.dataset_of_artists)