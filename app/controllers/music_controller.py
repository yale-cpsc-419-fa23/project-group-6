from flask import Blueprint, jsonify, request, render_template, redirect, flash, current_app, url_for
from werkzeug.utils import secure_filename
import os

from app.models.song import Song


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
        {"name": song.name, 
         "filepath": song.filepath, 
         "upload_date": song.upload_date.strftime('%Y-%m-%d',),
         "popularity": song.popularity,
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
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If user does not select file, browser might submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract features from song
        # features = audio_feature_extractor(file_path)
        features = {}
        song_details = {
            "name": request.form['name'],
            "filepath": file_path
        }
        song_data = {**song_details, **features}
        
        with current_app.app_context():
            # Add the song to the database
            song = Song.create(**song_data)
        
        flash('File successfully uploaded')
        return redirect(url_for('main.home'))
    else:
        flash('Allowed file types are mp3, wav, and flac')
        return redirect(request.url)
    