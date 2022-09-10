import music.search.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session

search_blueprint = Blueprint(
    'search_bp', __name__)



@search_blueprint.route('/search', methods=['GET'])
def search():
    return render_template('search/search.html')


@search_blueprint.route('/search_tracks', methods=['GET'])
def search_tracks():
    target_track = request.args.get('target_track')
    if target_track is "":
        return redirect(url_for('search_bp.search'))
    
    matching_tracks = services.get_tracks(target_track, repo.repo_instance)
    for track in matching_tracks:
        print(track.title)
        print(track.artist.full_name)
        print(track.album.title)
    
    if len(matching_tracks) > 0:
        return render_template('search/search_tracks.html', matching_tracks=matching_tracks)
    return render_template('search/search.html')