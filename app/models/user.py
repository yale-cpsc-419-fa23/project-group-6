from datetime import datetime
from app import db, create_app


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

    @classmethod
    def create(cls, username, password, email, gender = None, birthday = None):
        if cls.find_by_email(email) is not None:
            raise ValueError("Email already exists!")
        new_user = cls(username=username, password=password, email=email, gender=gender, birthday=birthday,
                       registeredDateTime=datetime.now())
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


if __name__ == "__main__":
    app = create_app('DevelopmentConfig')
    with app.app_context():
        U = User()
        print(U.find_by_id(100))
        # print(U.create("test", "test", "test@example.com"))
        print(U.find_by_email("test@example.com").userId)



