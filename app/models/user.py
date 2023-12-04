from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random

from app import db
from app.models.user_song_like import UserSongLike
from app.models.user_user_follow import UserUserFollow


class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Birthday = db.Column(db.Date, nullable=False)
    RegisteredDateTime = db.Column(db.DateTime, nullable=False)
    create_records = db.relationship(
        'UserSongCreate',
        backref='user'
    )
    like_records = db.relationship(
        'UserSongLike',
        order_by='UserSongLike.LikedDate.desc()',
        back_populates='user'
    )
    followed = db.relationship(
        'UserUserFollow',
        foreign_keys=[UserUserFollow.UserId1],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic'
    )
    followers = db.relationship(
        'UserUserFollow',
        foreign_keys=[UserUserFollow.UserId2],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f"<User {self.Username}>"

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    @classmethod
    def create(cls, username, password, email, gender=None, birthday=None):
        if cls.find_by_email(email) is not None:
            raise ValueError("Email already exists!")
        new_user = cls(Username=username, Email=email, Gender=gender, Birthday=birthday,
                       RegisteredDateTime=datetime.now())
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(Username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(Email=email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return db.session.get(cls, user_id)

    @classmethod
    def alter_by_id(cls, user_id, username, password, email, gender, birthday):
        user = db.session.get(cls, user_id)
        if not user:
            return None
        if username:
            user.Username = username
        if password:
            user.Password = password
        if email:
            user.Email = email
        if gender:
            user.Gender = gender
        if birthday:
            user.Birthday = birthday
        db.session.commit()
        return user

    # info retrieval
    def get_registered_date_time(self):
        registered_date_time = self.RegisteredDateTime

        return registered_date_time

    def get_id(self):
        return self.UserId

    def get_username(self):
        return self.Username

    def get_email(self):
        return self.Email

    def get_gender(self):
        return self.Gender

    def get_birthday(self):
        return self.Birthday

    def get_created_songs(self):
        return [record.get_song() for record in self.create_records]

    def get_liked_songs(self, n_likes):
        like_records = random.sample(self.like_records, min(n_likes, len(self.like_records)))
        return [record.get_song() for record in like_records]

    def is_liked_song(self, song_id):
        return any(like_record.SongId == song_id for like_record in self.like_records)

    def is_following(self, user_id):
        return any(follow_record.UserId2 == user_id for follow_record in self.followed)

    def is_followed_by(self, user_id):
        return any(follow_record.UserId1 == user_id for follow_record in self.followers)

    def get_followed(self):
        return [record.get_followed() for record in self.followed]

    def get_followers(self):
        return [record.get_follower() for record in self.followers]

    # info update
    def update_username(self, new_username):
        self.Username = new_username
        db.session.commit()

    def update_password(self, new_password):
        self.set_password(new_password)
        db.session.commit()

    def update_gender(self, new_gender):
        self.Gender = new_gender
        db.session.commit()

    def update_birthday(self, new_birthday):
        self.Birthday = new_birthday
        db.session.commit()

    def like(self, song_id):
        existing_like = any(like_record.SongId == song_id for like_record in self.like_records)
        if not existing_like:
            like_record = UserSongLike(UserId=self.UserId, SongId=song_id, LikedDate=datetime.now())
            self.like_records.append(like_record)
            db.session.commit()
            return True
        return False

    def unlike(self, song_id):
        like_record = next((like for like in self.like_records if like.SongId == song_id), None)
        if like_record:
            db.session.delete(like_record)
            db.session.commit()
            return True
        return False

    def follow(self, user_id):
        if not self.is_following(user_id):
            follow = UserUserFollow(UserId1=self.UserId, UserId2=user_id)
            db.session.add(follow)
            db.session.commit()
            return True
        return False

    def unfollow(self, user_id):
        follow_record_to_delete = next(
            (follow_record for follow_record in self.followed if follow_record.UserId2 == user_id), None)
        if follow_record_to_delete:
            db.session.delete(follow_record_to_delete)
            db.session.commit()
            return True
        return False
