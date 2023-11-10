from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from app import db
from app.models.song import Song


class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    registeredDateTime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @classmethod
    def create(cls, username, password, email, gender = None, birthday = None):
        if cls.find_by_email(email) is not None:
            raise ValueError("Email already exists!")
        new_user = cls(username=username, email=email, gender=gender, birthday=birthday,
                       registeredDateTime=datetime.now())
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return db.session.get(cls, user_id)

    @classmethod
    def alter_by_id(cls, user_id, username, password, email, gender, birthday):
        user = db.session.get(cls, user_id)
        if not user:
            return None
        if username:
            user.username = username
        if password:
            user.password = password
        if email:
            user.email = email
        if gender:
            user.gender = gender
        if birthday:
            user.birthday = birthday
        db.session.commit()
        return user

    def get_created_songs(self):
        # Fetching all UserSongCreate records associated with this user
        user_song_records = self.user_songs

        # Extracting song IDs from those records
        song_ids = [user_song.songId for user_song in user_song_records]

        # Fetching Song records corresponding to those IDs
        created_songs = Song.get_songs_by_ids(song_ids)
        return created_songs




