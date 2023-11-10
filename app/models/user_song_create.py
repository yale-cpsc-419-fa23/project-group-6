from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import db, create_app


class UserSongCreate(db.Model):
    songId = Column(Integer, ForeignKey('song.songId'), primary_key=True)
    userId = Column(Integer, ForeignKey('user.userId'), primary_key=True)

    user = relationship("User", backref="user_songs")
    song = relationship("Song", backref="song_users")

    def __repr__(self):
        return f"<UserSongCreate userId={self.userId}, songId={self.songId}>"

    @classmethod
    def get_user_song_ids(cls, user_id):
        return cls.query.filter_by(userId=user_id).all()