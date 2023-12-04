from flask import Blueprint, jsonify, request, render_template, redirect, flash, current_app, url_for, session
from werkzeug.utils import secure_filename
import os

from app.models.song import Song
from app.models.user import User
from app.models.genre import Genre
from app.models.user_song_create import UserSongCreate
from app.models.user_song_like import UserSongLike
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
        {
            "id": song.get_id(),
            "name": song.get_name(),
            "filepath": song.get_file_path(),
            "upload_date": song.get_upload_date().strftime('%Y-%m-%d'),
            "creators": song.get_creators_profiles(),
            "popularity": song.get_popularity(),
            "liked": song.is_liked_by_user(session.get("user_id")),
        } for song in songs
    ]

    return jsonify(songs_json)


@music.route('/liked_songs')
def liked_songs():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.find_by_id(user_id)
    liked_songs_records = user.like_records

    liked_songs = []
    for record in liked_songs_records:
        song = record.song
        liked_date = record.LikedDate
        creators = song.get_creators_profiles()
        liked_songs.append((song, liked_date, creators))

    return render_template('liked_songs.html', songs=liked_songs)


@music.route('/uploaded_songs')
def uploaded_songs():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.find_by_id(user_id)
    songs = user.get_created_songs()

    for song in songs:
        song.creators = song.get_creators_profiles()
    return render_template('uploaded_songs.html', songs=songs)


@music.route('/upload_song', methods=['GET'])
def upload_song():
    return render_template('upload.html')


@music.route('/save_song', methods=['POST'])
def save_song():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        features = audio_feature_extractor(file_path)
        song_details = {
            "Name": request.form['name'],
            "Filepath": file_path
        }
        song_data = {**song_details, **features}

        with current_app.app_context():
            song = Song.create(session.get("user_id"), **song_data)

        flash('File successfully uploaded', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Allowed file types are mp3, wav, and flac', 'danger')
        return redirect(request.url)


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

    return redirect(url_for('music.uploaded_songs'))


@music.route('/add-artists/<int:song_id>', methods=['POST'])
def add_artists(song_id):
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('auth.login'))

    song_to_update = Song.query.get(song_id)
    artist_ids = request.form['artist_ids'].split(',')

    if song_to_update:
        try:
            artist_id_list = [int(id.strip()) for id in artist_ids]
            valid_ids, invalid_ids = song_to_update.add_creators(artist_id_list)
            if valid_ids:
                flash(f'Artists {", ".join(map(str, valid_ids))} added successfully.', 'success')
            if invalid_ids:
                flash(f'Artists with IDs: {", ".join(map(str, invalid_ids))} are not valid and were not added.',
                      'error')
        except ValueError:
            flash('Invalid artist IDs provided.', 'error')
    else:
        flash('Song not found.')

    return redirect(url_for('music.uploaded_songs'))


@music.route('/search-genre', methods=['GET'])
def search_genre():
    genre_name = request.args.get('genre_name')
    genres = Genre.find_by_name(genre_name)
    genres_json = [{"Name": genre.get_genre_name()} for genre in genres]
    return jsonify(genres_json)


@music.route('/top-songs-by-genre', methods=['GET'])
def top_songs_by_genre():
    genre_name = request.args.get('genre')
    top_songs = Genre.get_top_songs(genre_name, limit=20)

    if top_songs:
        songs_json = [
            {
                "name": song.get_name(),
                "creators": song.get_creators_profiles(),
                "popularity": song.get_popularity()
            } for song in top_songs
        ]
        return jsonify(songs_json)
    else:
        return jsonify([])


@music.route('/like_song', methods=['POST'])
def like_song():
    song_id = request.json.get('song_id')
    user_id = session.get("user_id")
    user = User.find_by_id(user_id)
    if user.like(song_id):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Already liked"}), 400


@music.route('/unlike_song', methods=['POST'])
def unlike_song():
    song_id = request.json.get('song_id')
    user_id = session.get("user_id")
    user = User.find_by_id(user_id)
    if user.unlike(song_id):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Not liked"}), 400
