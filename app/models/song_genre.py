from app import db
from app.models.genre import Genre
from app.models.song import Song


class SongGenre(db.Model):
    SongId = db.Column(db.Integer, db.ForeignKey('song.SongId'), primary_key=True)
    GenreId = db.Column(db.Integer, db.ForeignKey('genre.GenreId'), primary_key=True)
