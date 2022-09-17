import music.view.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session

view_blueprint = Blueprint(
    'view_bp', __name__)


@view_blueprint.route('/view_track', methods=['GET'])
def view_track():
    track_id = request.args.get('track_id')
    track = services.get_track_by_id(int(track_id), repo.repo_instance)
    print(track)
    return render_template('view/view_track.html', track=track)
