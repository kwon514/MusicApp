import music.playlist.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from music.authentication.authentication import login_required

playlist_blueprint = Blueprint(
    'playlist_bp', __name__)

@playlist_blueprint.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    user_name = session['user_name']
    form = CreatePlaylistForm()
    playlist_name_not_unique = None
    try:
        services.get_user(user_name, repo.repo_instance)
    except services.UnknownUserException:
        return redirect(url_for('authentication_bp.login')) 
    if form.validate_on_submit():
        try:
            playlist_name = form.playlist_name.data
            services.add_playlist(playlist_name, user_name, repo.repo_instance)
            return redirect(url_for('playlist_bp.get_playlists'))
        except services.PlaylistNotUniqueException:
            playlist_name_not_unique = 'Your playlist name is already taken - please supply another'
    return render_template(
        'playlist/create_playlist.html',
        title='Create Playlist',
        form=form,
        playlist_name_error_message = playlist_name_not_unique,
        )


@playlist_blueprint.route('/playlists', methods=['GET'])
@login_required
def get_playlists():
    user_name = session['user_name']
    try:
        playlists = services.get_playlists(user_name, repo.repo_instance)
    except services.UnknownUserException:
        return redirect(url_for('authentication_bp.login')) 
    return render_template('playlist/playlists.html', playlists=playlists)

# @playlist_blueprint.route('/playlist', methods=['GET'])
# def playlist():
#     target_track = request.args.get('target_playlist')
#     if target_playlist == "":
#         return redirect(url_for('search_bp.search'))
#     matching_tracks = services.get_tracks(target_track, repo.repo_instance)
#     if len(matching_tracks) > 0:
#         return render_template('search/search_results.html', search_by='track', target=target_track, matches=matching_tracks)
#     return render_template('search/search_tracks.html')

class CreatePlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist', [
        DataRequired()])
    submit = SubmitField('Create')   