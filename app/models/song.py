import random
from datetime import datetime
from sqlalchemy.sql.expression import func
from app import db
from app.models.user_song_create import UserSongCreate
from app.models.genre import Genre

class Song(db.Model):
    SongId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Duration_ms = db.Column(db.Integer)
    Explicit = db.Column(db.Integer)
    Mode = db.Column(db.Integer)
    Key = db.Column(db.Integer)
    Tempo = db.Column(db.Float)
    Energy = db.Column(db.Float)
    Danceability = db.Column(db.Float)
    Loudness = db.Column(db.Float)
    Acousticness = db.Column(db.Float)
    Instrumentalness = db.Column(db.Float)
    Liveness = db.Column(db.Float)
    Speechiness = db.Column(db.Float)
    Valence = db.Column(db.Float)
    Popularity = db.Column(db.Integer)
    Filepath = db.Column(db.Text)
    Cluster = db.Column(db.Integer)

    genres = db.relationship('Genre', secondary='song_genre', back_populates='songs')
    create_records = db.relationship('UserSongCreate', backref='song')
    like_records = db.relationship('UserSongLike', back_populates='song')

    def __repr__(self):
        return f"<Song {self.SongId}>"

    @classmethod
    def create(cls, user_id, **kwargs):
        song = cls(Popularity=0, **kwargs)
        db.session.add(song)
        db.session.commit()
        user_song = UserSongCreate(UserId=user_id, SongId=song.SongId, UploadDate=datetime.now(),
                                   EditDate=datetime.now())
        db.session.add(user_song)
        db.session.commit()

        return song

    @classmethod
    def search_by_id(cls, song_id, increment_popularity=False):
        song = db.session.get(cls, song_id)
        if song and increment_popularity:
            song.Popularity += 1
            db.session.commit()
        return song

    @classmethod
    def search_by_name(cls, name, increment_popularity=False, limit=100):
        query = cls.query.filter(cls.Name.ilike(f"%{name}%"))

        if increment_popularity:
            for song in query.all():
                song.Popularity += 1
            db.session.commit()

        query = query.order_by(cls.Popularity.desc())
        if limit:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def get_songs_by_ids(cls, song_ids):
        if not song_ids:
            return []
        return cls.query.filter(cls.SongId.in_(song_ids)).all()
    
    @classmethod
    def get_top_songs(cls, limit=20):
        return cls.query.order_by(cls.Popularity.desc()).limit(limit).all()

    @classmethod
    def get_all_songs(cls, n=None):
        if n is None:
            return db.session.query(cls).all()
        return db.session.query(cls).order_by(func.random()).limit(n).all()
    
    def rename(self, name):
        self.Name = name

        user_song_records = self.create_records
        for record in user_song_records:
            record.EditDate = datetime.now()

        db.session.commit()

    def get_upload_date(self):
        if self.create_records:
            return min(record.UploadDate for record in self.create_records)
        return None

    def get_name(self):
        return self.Name

    def get_popularity(self):
        return self.Popularity

    def get_file_path(self):
        return self.Filepath

    def get_genres(self):
        return self.genres

    def get_creators(self):
        return [record.get_creator() for record in self.create_records]

    def get_id(self):
        return self.SongId

    def add_creators(self, user_ids):
        for user_id in user_ids:
            existing_record = UserSongCreate.query.filter_by(UserId=user_id, SongId=self.SongId).first()
            if not existing_record:
                user_song = UserSongCreate(UserId=user_id, SongId=self.SongId,
                                           UploadDate=datetime.now(), EditDate=datetime.now())
                db.session.add(user_song)
            else:
                existing_record.EditDate = datetime.now()
        db.session.commit()

    def add_genres(self, genres):
        for genre in genres:
            if genre not in self.genres:
                self.genres.append(genre)
        db.session.commit()

    def set_cluster(self, cluster):
        self.Cluster = cluster
        db.session.commit()

    def is_liked_by_user(self, user_id):
        return any(like.UserId == user_id for like in self.like_records)