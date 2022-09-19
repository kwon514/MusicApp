import music.search.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search_tracks', methods=['GET'])
def search_tracks():
    return render_template('search/search_tracks.html')

@search_blueprint.route('/search_artists', methods=['GET'])
def search_artists():
    return render_template('search/search_artists.html')

@search_blueprint.route('/search_albums', methods=['GET'])
def search_albums():
    return render_template('search/search_albums.html')


@search_blueprint.route('/search_tracks_result', methods=['GET'])
def search_tracks_result():
    target_track = request.args.get('target_track')
    if target_track == "":
        return redirect(url_for('search_bp.search_tracks'))
    matching_tracks = services.get_tracks(target_track, repo.repo_instance)
    playlists = services.get_playlists_without_username(repo.repo_instance)
    if len(matching_tracks) > 0:
        return render_template('search/search_results.html', search_by='track', target=target_track, matches=matching_tracks, playlists=playlists)
    return render_template('search/search_tracks.html')

@search_blueprint.route('/search_artists_result', methods=['GET'])
def search_artists_result():
    target_artist = request.args.get('target_artist')
    if target_artist == "":
        return redirect(url_for('search_bp.search'))
    matching_artists = services.get_artists(target_artist, repo.repo_instance)
    playlists = services.get_playlists_without_username(repo.repo_instance)
    if len(matching_artists) > 0:
        return render_template('search/search_results.html', search_by='artist', target=target_artist, matches=matching_artists, playlists=playlists)
    return render_template('search/search_artists.html')

@search_blueprint.route('/search_albums_result', methods=['GET'])
def search_albums_result():
    target_album = request.args.get('target_album')
    if target_album == "":
        return redirect(url_for('search_bp.search'))
    matching_albums = services.get_albums(target_album, repo.repo_instance)
    playlists = services.get_playlists_without_username(repo.repo_instance)
    if len(matching_albums) > 0:
        return render_template('search/search_results.html', search_by='album', target=target_album, matches=matching_albums, playlists=playlists)
    return render_template('search/search_albums.html')
