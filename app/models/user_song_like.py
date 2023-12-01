from app import db

from datetime import datetime

class UserSongLike(db.Model):
    SongId = db.Column(db.Integer, db.ForeignKey('song.SongId'), primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId'), primary_key=True)
    LikedDate = db.Column(db.DateTime)

    song = db.relationship('Song', back_populates='like_records')

    @staticmethod
    def get_liked_songs(user_id):
        liked_songs_records = UserSongLike.query.filter_by(UserId=user_id).all()
        liked_songs = [(record.song, record.LikedDate) for record in liked_songs_records]

        return liked_songs
    
    @staticmethod
    def like_song(user_id, song_id):
        if not UserSongLike.query.get((song_id, user_id)):
            like = UserSongLike(SongId=song_id, UserId=user_id, LikedDate=datetime.now())
            db.session.add(like)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def unlike_song(user_id, song_id):
        like = UserSongLike.query.get((song_id, user_id))
        if like:
            db.session.delete(like)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f"<UserSongLike UserId={self.UserId}, SongId={self.SongId}>"

    def get_song(self):
        return self.song

    def get_creator(self):
        return self.user
    
    def get_liked_date(self):
        return self.LikedDate
    