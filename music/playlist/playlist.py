import music.playlist.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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
        playlist_name_error_message=playlist_name_not_unique,
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


@playlist_blueprint.route('/playlist/<playlist_name>', methods=['GET', 'POST'])
@login_required
def playlist(playlist_name):
    user_name = session['user_name']
    copy_playlist = CopyPlaylistForm()
    playlist_name_not_unique = None

    try:
        playlist = services.get_playlist(
            playlist_name, user_name, repo.repo_instance)
    except services.UnknownUserException:
        return redirect(url_for('authentication_bp.login'))

    list_of_tracks = playlist.list_of_tracks()

    if copy_playlist.is_submitted():
        try:
            services.create_playlist_from_list(
                playlist_name, list_of_tracks, user_name, repo.repo_instance)
        except services.PlaylistNotUniqueException:
            playlist_name_not_unique = 'There is already a copy of this playlist!'

    return render_template('playlist/playlist.html',
                           playlist_name=playlist.playlist_name,
                           list_of_tracks=list_of_tracks, copy_playlist=copy_playlist, playlist_name_error_message=playlist_name_not_unique)


@playlist_blueprint.route('/add_track/<playlist_name>/<int:track_id>', methods=['GET', 'POST'])
@login_required
def add_track(playlist_name, track_id):
    try:
        track = services.get_track_by_id(track_id, repo.repo_instance)
        services.add_track(track, playlist_name, repo.repo_instance)
    except services.UnknownUserException:
        return redirect(url_for('authentication_bp.login'))
    return redirect(request.referrer)


class CreatePlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist', [
        DataRequired()])
    submit = SubmitField('Create')


class CopyPlaylistForm(FlaskForm):
    button = SubmitField('Copy Playlist', render_kw={
                         "onclick": "showDupeToast()"})
