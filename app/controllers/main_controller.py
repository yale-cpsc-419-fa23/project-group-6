from flask import Blueprint, render_template, session, flash, redirect, url_for

from app.models.song import Song
from app.utils.recommendation_utils import recommend_songs

main = Blueprint('main', __name__)

@main.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('home.html')

@main.route('/explore')
def explore():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    top_songs = Song.get_top_songs()
    recommendation_info, recommended_songs = recommend_songs(session['user_id'], n_likes=5, n_recommendations=5)

    for recommended_song in recommended_songs:
        recommended_song.creators = ", ".join([creator.get_username() for creator in recommended_song.get_creators()])

    return render_template('explore.html',
                           top_songs=top_songs,
                           recommended_songs=recommended_songs,
                           recommendation_info=recommendation_info)

