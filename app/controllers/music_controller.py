from flask import Blueprint, jsonify, request

from app.models.song import Song


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
