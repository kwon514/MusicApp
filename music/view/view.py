import music.view.services as services
import music.adapters.repository as repo

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from music.domainmodel.review import Review


view_blueprint = Blueprint(
    'view_bp', __name__)


@view_blueprint.route('/view_track', methods=['GET', 'POST'])
def view_track():
    track_id = request.args.get('track_id')
    track = services.get_track_by_id(int(track_id), repo.repo_instance)
    playlists = []
    
    try:
        user_name = session['user_name']
        playlists = services.get_playlists(user_name, repo.repo_instance)
    except KeyError:
        pass
    
    review_form = ReviewForm()
    if review_form.is_submitted():
        review = Review(track, review_form.review_input.data, review_form.rating.data)
        services.add_review(review, repo.repo_instance)
        return redirect(url_for('view_bp.view_track', track_id=track_id))
    reviews = services.get_review(track, repo.repo_instance)
    reviews.reverse()
    
    return render_template('view/view_track.html', track=track, review_form=review_form, reviews=reviews, playlists=playlists)
class ReviewForm(FlaskForm):
    review_input = TextAreaField('Review', [DataRequired(), Length(min=1, max=1000)])
    rating = SelectField('Rating', choices=[1, 2, 3, 4, 5], coerce=int)
    submit = SubmitField('Submit') 