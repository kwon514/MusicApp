import music.playlist.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

playlist_blueprint = Blueprint(
    'playlist_bp', __name__)

@playlist_blueprint.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    form = CreatePlaylistForm()
    playlist_name_not_unique = None
    if form.validate_on_submit():
        try:
            playlist_name = form.playlist_name.data
            services.add_playlist(playlist_name, repo.repo_instance)
            return redirect(url_for('playlist_bp.get_playlists'))
        except services.PlaylistNotUniqueException:
            playlist_name_not_unique = 'Your playlist name is already taken - please supply another'

    return render_template(
        'playlist/create_playlist.html',
        title='Create Playlist',
        form=form,
        playlist_name_error_message = playlist_name_not_unique
        )


@playlist_blueprint.route('/playlists', methods=['GET'])
def get_playlists():
    playlists = services.get_playlists(repo.repo_instance)
    return render_template('playlist/playlists.html', playlists=playlists)


class CreatePlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist', [
        DataRequired()])
    submit = SubmitField('Create')   