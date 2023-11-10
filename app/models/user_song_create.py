from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import db, create_app


class UserSongCreate(db.Model):
    __tablename__ = 'user_song_create_dg_tmp'

    songId = Column(Integer, ForeignKey('song.songId'), primary_key=True)
    userId = Column(Integer, ForeignKey('user.userId'), primary_key=True)

    user = relationship("User", backref="user_songs")
    song = relationship("Song", backref="song_users")

    def __repr__(self):
        return f"<UserSongCreate userId={self.userId}, songId={self.songId}>"

    def create(cls, user_id, song_id):
        user_song = cls(userId=user_id, songId=song_id)
        db.session.add(user_song)
        db.session.commit()
        return user_song