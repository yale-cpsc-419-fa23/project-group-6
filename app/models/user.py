from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from app import db
from app.models.song import Song


class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Birthday = db.Column(db.Date, nullable=False)
    RegisteredDateTime = db.Column(db.DateTime, nullable=False)

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

    def get_created_songs(self):
        # Fetching all UserSongCreate records associated with this user
        user_song_records = self.user_songs

        # Extracting song IDs from those records
        song_ids = [user_song.SongId for user_song in user_song_records]

        # Fetching Song records corresponding to those IDs
        created_songs = Song.get_songs_by_ids(song_ids)
        return created_songs
    
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

    def get_registered_date_time(self):
        registered_date_time = self.RegisteredDateTime

        return registered_date_time

    def get_user_name(self):
        return self.Username

    def get_email(self):
        return self.Email

    def get_gender(self):
        return self.Gender
    
    def get_birthday(self):
        return self.Birthday