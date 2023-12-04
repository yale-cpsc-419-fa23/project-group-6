from app import db


class Genre(db.Model):
    GenreId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String)
    Description = db.Column(db.Text)
    songs = db.relationship(
        'Song',
        secondary='song_genre',
        back_populates='genres',
        order_by='Song.Popularity.desc()'
    )

    @classmethod
    def create_genres(cls, genre_names):
        genres = []
        for genre_name in genre_names:
            genre = Genre.query.filter_by(Name=genre_name).first()
            if not genre:
                genre = Genre(Name=genre_name)
                db.session.add(genre)
                db.session.commit()
            genres.append(genre)
        return genres

    @classmethod
    def get_all_genre(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, genre_id):
        return cls.query.get(genre_id)

    @classmethod
    def find_by_name(cls, genre_name, precise=False):
        if precise:
            return cls.query.filter_by(Name=genre_name).first()
        return cls.query.filter(cls.Name.like(f"%{genre_name}%"))

    @classmethod
    def get_top_songs(cls, genre_name, limit=20):
        genre = cls.query.filter_by(Name=genre_name).first()
        if genre is not None:
            return genre.songs[:limit]
        else:
            return []

    def __repr__(self):
        return self.Name

    def get_genre_name(self):
        return self.Name

    def get_genre_description(self):
        return self.Description

    def get_songs(self):
        return self.songs
