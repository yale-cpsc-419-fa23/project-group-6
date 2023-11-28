from app import db

song_genre = db.Table('song_genre',
    db.Column('SongId', db.Integer, db.ForeignKey('song.SongId'), primary_key=True),
    db.Column('GenreId', db.Integer, db.ForeignKey('genre.GenreId'), primary_key=True)
)