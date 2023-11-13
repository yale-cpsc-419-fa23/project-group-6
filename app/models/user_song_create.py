from app import db


class UserSongCreate(db.Model):
    SongId = db.Column(db.Integer, db.ForeignKey('song.SongId'), primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId'), primary_key=True)
    UploadDate = db.Column(db.DateTime)
    EditDate = db.Column(db.DateTime)

    user = db.relationship("User", backref="user_songs")
    song = db.relationship("Song", backref="song_users")

    def __repr__(self):
        return f"<UserSongCreate UserId={self.UserId}, SongId={self.SongId}>"

    @classmethod
    def get_user_song_ids(cls, user_id):
        return cls.query.filter_by(UserId=user_id).all()