import os

from flask import Blueprint, jsonify, request, render_template, redirect, flash, current_app, url_for, session
from werkzeug.utils import secure_filename
import os

from app.models.song import Song
from app.models.user import User
from app.models.genre import Genre
from app.models.user_song_create import UserSongCreate
from app.utils.audio_feature_utils import audio_feature_extractor

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

music = Blueprint('music', __name__)


@music.route('/search', methods=['GET'])
def search():
    song_name = request.args.get('song_name')
    increment_popularity = request.args.get('increment_popularity', 'false') == 'true'

    if not song_name:
        return jsonify([])

    songs = Song.search_by_name(song_name, increment_popularity, limit=10 if not increment_popularity else 100)
    songs_json = [
        {"name": song.get_name(),
         "filepath": song.get_file_path(),
         "upload_date": song.get_upload_date().strftime('%Y-%m-%d', ),
         "upload_user": song.get_creators()[0].get_username(),
         "popularity": song.get_popularity(),
         } for song in songs]

    return jsonify(songs_json)


@music.route('/upload_song', methods=['GET'])
def upload_song():
    return render_template('upload.html')


@music.route('/save_song', methods=['POST'])
def save_song():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    file = request.files['file']
    # If user does not select file, browser might submit an empty part without filename
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract features from song
        features = audio_feature_extractor(file_path)
        # features = {}
        song_details = {
            "Name": request.form['name'],
            "Filepath": file_path
        }
        song_data = {**song_details, **features}

        with current_app.app_context():
            # Add the song to the database
            song = Song.create(session.get("user_id"), **song_data) #TODO: Add user_id to the function call

        flash('File successfully uploaded', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Allowed file types are mp3, wav, and flac', 'danger')
        return redirect(request.url)


@music.route('/my-songs')
def my_songs():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.find_by_id(user_id)
    songs = user.get_created_songs()

    return render_template('my_songs.html', songs=songs)


@music.route('/rename-song/<int:song_id>', methods=['POST'])
def rename_song(song_id):
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('auth.login'))

    song_to_rename = Song.query.get(song_id)
    new_name = request.form['new_name']

    if song_to_rename:
        song_to_rename.rename(new_name)
        flash('Song renamed successfully.')
    else:
        flash('Song not found.')

    return redirect(url_for('music.my_songs'))


@music.route('/search-genre', methods=['GET'])
def search_genre():
    genre_name = request.args.get('genre_name')
    genres = Genre.find_by_name(genre_name)
    genres_json = [{"Name": genre.get_genre_name()} for genre in genres]
    return jsonify(genres_json)
