from app import db


class UserSongLike(db.Model):
    SongId = db.Column(db.Integer, db.ForeignKey('song.SongId'), primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId'), primary_key=True)
    LikedDate = db.Column(db.DateTime)

    def __repr__(self):
        return f"<UserSongLike UserId={self.UserId}, SongId={self.SongId}>"

    def get_song(self):
        return self.song

    def get_creator(self):
        return self.user