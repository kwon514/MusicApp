import music.search.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.is_submitted():
        query = search_form.query.data
        search_by = search_form.search_by.data
        return redirect(url_for('search_bp.search_results', query=query, search_by=search_by))
    return render_template('search/search.html', search_form=search_form)


@search_blueprint.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('query')
    results = request.args.get('results')
    playlists = request.args.get('playlists')
    search_by = request.args.get('search_by')
    
    if search_by == "track":
        results = services.get_tracks(query, repo.repo_instance)
    elif search_by == "artist":
        results = services.get_artists(query, repo.repo_instance)
    elif search_by == "album":
        results = services.get_albums(query, repo.repo_instance)
    elif search_by == "genre":
        results = services.get_genres(query, repo.repo_instance)
    else:
        # This should never happen.
        return redirect(url_for('search_bp.search'))

    return render_template('search/search_results.html', query=query, search_by=search_by, results=results, playlists=playlists)


class SearchForm(FlaskForm):
    query = StringField('Search', [DataRequired()])
    search_by = SelectField(
        'Rating', choices=[("track", "Track"), ("artist", "Artist"), ("album", "Album"), ("genre", "Genre")], coerce=str)
    submit = SubmitField('Search')
